"""LLM agent utilities for structured output."""

import base64
import json
import logging
import os
import re
import subprocess
import tempfile
from typing import Any, Dict, Optional, TypeVar, Type

from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
from pathlib import Path
from pydantic import ValidationError

logger = logging.getLogger(__name__)

T = TypeVar('T')

# Models named "codex:<model>" are run through the Codex CLI (`codex exec`), which
# bills against the ChatGPT subscription it is logged in with instead of the API.
CODEX_PREFIX = "codex:"
# Codex caps a turn's input at 1,048,576 chars; leave room for instructions and schema.
CODEX_MAX_BODY_CHARS = 1_000_000


# Models named "claude:<model>" (e.g. claude:claude-opus-5-5) are run through the Claude Code
# CLI (`claude -p`), which bills against the Claude subscription it is logged in with.
CLAUDE_PREFIX = "claude:"


def is_codex_model(model: str) -> bool:
    return model.startswith(CODEX_PREFIX)


def is_claude_cli_model(model: str) -> bool:
    return model.startswith(CLAUDE_PREFIX)


def is_cli_model(model: str) -> bool:
    """True for models served by a logged-in CLI (no API key needed)."""
    return is_codex_model(model) or is_claude_cli_model(model)


class ClaudeCodeAgent:
    """Minimal stand-in for a LangChain agent that answers via the Claude Code CLI (`claude -p`).

    Same interface as CodexAgent: `invoke({"messages": [...]})` returns a dict with
    "structured_response" (when response_format is set) or "output". Messages are sent as one
    stream-json user turn, so image blocks reach Claude as images; structured output uses the
    CLI's --json-schema validation. Built-in tools, MCP servers and settings files are disabled
    and the session runs in an empty temp dir, so Claude acts as a plain judge.
    """

    def __init__(self, model: str, system_prompt: str, response_format: Optional[Type[T]] = None,
                 max_attempts: int = 3, timeout: int = 900):
        self.model = model[len(CLAUDE_PREFIX):]
        self.system_prompt = system_prompt
        self.response_format = response_format
        self.max_attempts = max_attempts
        self.timeout = int(os.getenv("CLAUDE_TIMEOUT", timeout))
        self.effort = os.getenv("CLAUDE_EFFORT")

    @staticmethod
    def _content_blocks(messages: list) -> list[dict]:
        """Convert chat messages (LangChain/OpenAI or Anthropic style) into Anthropic content blocks."""
        blocks = []
        for msg in messages:
            content = msg.get("content") if isinstance(msg, dict) else getattr(msg, "content", msg)
            role = msg.get("role", "user") if isinstance(msg, dict) else "user"
            if isinstance(content, str):
                blocks.append({"type": "text", "text": content if role == "user" else f"[{role}]\n{content}"})
                continue
            for block in content:
                if block.get("type") == "text":
                    blocks.append({"type": "text", "text": block["text"]})
                elif block.get("type") == "image" and block.get("source", {}).get("type") == "base64":
                    blocks.append({"type": "image", "source": block["source"]})
                elif block.get("type") == "image_url":
                    url = block["image_url"]["url"] if isinstance(block["image_url"], dict) else block["image_url"]
                    media_type, data = re.match(r"data:([^;]+);base64,(.*)", url, re.S).groups()
                    blocks.append({"type": "image",
                                   "source": {"type": "base64", "media_type": media_type, "data": data}})
                else:
                    raise ValueError(f"Unsupported content block for Claude backend: {block.get('type')}")
        return blocks

    def _run_claude(self, blocks: list[dict], workdir: Path) -> dict:
        cmd = [
            "claude", "-p",
            "--model", self.model,
            "--system-prompt", self.system_prompt,
            "--tools", "",
            "--strict-mcp-config",
            "--setting-sources", "",
            "--no-session-persistence",
            "--input-format", "stream-json",
            "--output-format", "stream-json", "--verbose",
        ]
        if self.effort:
            cmd += ["--effort", self.effort]
        if self.response_format is not None:
            cmd += ["--json-schema", json.dumps(self.response_format.model_json_schema())]
        turn = json.dumps({"type": "user", "message": {"role": "user", "content": blocks}})
        proc = subprocess.run(cmd, input=turn + "\n", capture_output=True, text=True,
                              timeout=self.timeout, cwd=workdir)
        result = None
        for line in proc.stdout.splitlines():
            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                continue
            if event.get("type") == "result":
                result = event
        if result is None or result.get("is_error") or proc.returncode != 0:
            detail = (result or {}).get("result") or proc.stderr.strip()[-2000:] or proc.stdout.strip()[-2000:]
            raise RuntimeError(f"claude -p failed (rc={proc.returncode}): {detail}")
        return result

    def invoke(self, inputs: dict) -> dict:
        messages = inputs["messages"] if isinstance(inputs, dict) else inputs
        blocks = self._content_blocks(messages)
        with tempfile.TemporaryDirectory(prefix="claude_eval_") as tmp:
            if self.response_format is None:
                return {"output": self._run_claude(blocks, Path(tmp)).get("result", "")}

            last_error = None
            for _ in range(self.max_attempts):
                result = self._run_claude(blocks, Path(tmp))
                payload = result.get("structured_output")
                try:
                    if payload is None:
                        parsed = self.response_format.model_validate_json(
                            CodexAgent._extract_json(result.get("result") or ""))
                    else:
                        parsed = self.response_format.model_validate(payload)
                    return {"structured_response": parsed, "output": result.get("result", "")}
                except ValidationError as e:
                    last_error = e
                    logger.warning(f"Claude reply did not match {self.response_format.__name__}, retrying: {e}")
            raise ValueError(f"Claude reply never matched {self.response_format.__name__}: {last_error}")


class CodexAgent:
    """Minimal stand-in for a LangChain agent that answers via `codex exec`.

    Supports what the evaluation code uses: `invoke({"messages": [...]})` returning
    a dict with "structured_response" (when response_format is set) or "output".
    """

    def __init__(self, model: str, system_prompt: str, response_format: Optional[Type[T]] = None,
                 max_attempts: int = 3, timeout: int = 900):
        self.model = model[len(CODEX_PREFIX):]
        self.system_prompt = system_prompt
        self.response_format = response_format
        self.max_attempts = max_attempts
        self.timeout = int(os.getenv("CODEX_TIMEOUT", timeout))
        self.reasoning_effort = os.getenv("CODEX_REASONING_EFFORT")

    def _render(self, messages: list, image_dir: Path) -> tuple[str, list[str]]:
        """Flatten chat messages into one prompt; write images to files for `--image`."""
        parts, images = [], []
        for msg in messages:
            content = msg.get("content") if isinstance(msg, dict) else getattr(msg, "content", msg)
            role = msg.get("role", "user") if isinstance(msg, dict) else "user"
            if isinstance(content, str):
                parts.append(content if role == "user" else f"[{role}]\n{content}")
                continue
            for block in content:
                if block.get("type") == "text":
                    parts.append(block["text"])
                    continue
                if block.get("type") == "image" and block.get("source", {}).get("type") == "base64":
                    data, media_type = block["source"]["data"], block["source"].get("media_type", "image/png")
                elif block.get("type") == "image_url":
                    url = block["image_url"]["url"] if isinstance(block["image_url"], dict) else block["image_url"]
                    media_type, data = re.match(r"data:([^;]+);base64,(.*)", url, re.S).groups()
                else:
                    raise ValueError(f"Unsupported content block for Codex backend: {block.get('type')}")
                path = image_dir / f"image_{len(images) + 1}.{media_type.split('/')[-1]}"
                path.write_bytes(base64.b64decode(data))
                images.append(str(path))
                parts.append(f"[Attached image #{len(images)}]")
        return "\n\n".join(parts), images

    def _build_prompt(self, body: str) -> str:
        if len(body) > CODEX_MAX_BODY_CHARS:
            # Codex rejects inputs over 1,048,576 chars; keep the start and end of the body.
            half = CODEX_MAX_BODY_CHARS // 2
            logger.warning(f"Codex prompt body is {len(body):,} chars; truncating to {CODEX_MAX_BODY_CHARS:,}")
            body = f"{body[:half]}\n\n[... {len(body) - 2 * half:,} characters omitted ...]\n\n{body[-half:]}"
        prompt = (
            "You are being used as a plain LLM, not a coding agent: do not run commands, read files "
            "or browse. Answer only from the content below.\n\n"
            f"# Instructions\n{self.system_prompt}\n\n# Input\n{body}"
        )
        if self.response_format is not None:
            schema = json.dumps(self.response_format.model_json_schema(), indent=2)
            prompt += (
                "\n\n# Output format\nReply with a single JSON object that validates against this "
                f"JSON Schema, and nothing else (no prose, no code fences):\n{schema}"
            )
        return prompt

    def _run_codex(self, prompt: str, images: list[str], workdir: Path) -> str:
        out_file = workdir / "last_message.txt"
        cmd = [
            "codex", "exec",
            "--model", self.model,
            "--sandbox", "read-only",
            "--ephemeral", "--skip-git-repo-check", "--ignore-user-config", "--ignore-rules",
            "--color", "never",
            "--cd", str(workdir),
            "--output-last-message", str(out_file),
        ]
        if self.reasoning_effort:
            cmd += ["-c", f'model_reasoning_effort="{self.reasoning_effort}"']
        for img in images:
            cmd += ["--image", img]
        cmd.append("-")  # read prompt from stdin
        proc = subprocess.run(cmd, input=prompt, capture_output=True, text=True, timeout=self.timeout)
        if proc.returncode != 0 or not out_file.exists():
            # stderr echoes the whole prompt; surface the error lines rather than its tail.
            errors = [l for l in proc.stderr.splitlines() if l.startswith(("ERROR", "Error"))]
            detail = "\n".join(errors) if errors else proc.stderr.strip()[-2000:]
            raise RuntimeError(f"codex exec failed (rc={proc.returncode}): {detail}")
        return out_file.read_text()

    @staticmethod
    def _extract_json(text: str) -> str:
        fenced = re.search(r"```(?:json)?\s*(.*?)```", text, re.S)
        if fenced:
            return fenced.group(1)
        start, end = text.find("{"), text.rfind("}")
        return text[start:end + 1] if start != -1 and end > start else text

    def invoke(self, inputs: dict) -> dict:
        messages = inputs["messages"] if isinstance(inputs, dict) else inputs
        with tempfile.TemporaryDirectory(prefix="codex_eval_") as tmp:
            workdir = Path(tmp)
            body, images = self._render(messages, workdir)
            prompt = self._build_prompt(body)
            if self.response_format is None:
                return {"output": self._run_codex(prompt, images, workdir)}

            last_error = None
            for _ in range(self.max_attempts):
                text = self._run_codex(prompt, images, workdir)
                try:
                    parsed = self.response_format.model_validate_json(self._extract_json(text))
                    return {"structured_response": parsed, "output": text}
                except ValidationError as e:
                    last_error = e
                    logger.warning(f"Codex reply did not match {self.response_format.__name__}, retrying: {e}")
            raise ValueError(f"Codex reply never matched {self.response_format.__name__}: {last_error}")


def create_llm_agent(
    model: str,
    system_prompt: str,
    response_format: Optional[Type[T]] = None,
    tools: Optional[list] = None,
    temperature: float = 0.0,
    **kwargs: Any,
) -> Any:
    """Create an LLM agent with structured output support.
    
    Supports OpenAI (direct), OpenRouter (for third-party models), the Codex CLI
    (ChatGPT subscription) and the Claude Code CLI (Claude subscription).

    Args:
        model: Model name
            - OpenAI direct: "gpt-4o", "gpt-3.5-turbo", etc.
            - OpenRouter: "anthropic/claude-3.5-sonnet", "google/gemini-pro", etc.
            - Codex CLI: "codex:gpt-5.6-sol", etc. (tools and temperature are ignored)
            - Claude Code CLI: "claude:claude-opus-5-5", etc. (tools and temperature are ignored)
        system_prompt: System prompt for the agent
        response_format: Optional Pydantic model for structured output
        tools: Optional list of tools for the agent
        temperature: Temperature for LLM sampling (default: 0.0 for deterministic results)
        **kwargs: Additional LLM parameters (e.g., max_tokens, top_p)
    
    Returns:
        Configured agent
    """
    if is_codex_model(model):
        return CodexAgent(model, system_prompt, response_format)
    if is_claude_cli_model(model):
        return ClaudeCodeAgent(model, system_prompt, response_format)

    # Initialize the chat model with temperature and other parameters
    chat_model = init_chat_model(model, temperature=temperature, **kwargs)
    
    return create_agent(
        model=chat_model,
        tools=tools or [],
        system_prompt=system_prompt,
        response_format=response_format
    )


def invoke_structured_agent(
    agent,
    prompt: str | list | dict,
    response_model: Type[T]
) -> T:
    """
    Invoke an agent and extract structured output.
    
    Args:
        agent: LLM agent
        prompt: User prompt (str), messages list, or dict with "messages" key
        response_model: Pydantic model class for structured output
    
    Returns:
        Validated Pydantic model instance
    
    Raises:
        ValueError: If response cannot be validated
    """
    # Handle different input formats
    if isinstance(prompt, str):
        # Simple string prompt
        messages = [{"role": "user", "content": prompt}]
    elif isinstance(prompt, list):
        # List of messages
        messages = prompt
    elif isinstance(prompt, dict):
        # Dict with messages or direct invoke input
        if "messages" in prompt:
            messages = prompt["messages"]
        else:
            messages = prompt
    else:
        raise ValueError(f"Unsupported prompt type: {type(prompt)}")
    
    result = agent.invoke({"messages": messages})
    
    # Extract structured output from agent response
    # LangChain agents with response_format return structured output in "structured_response" key
    # Fall back to "output" if "structured_response" is not present
    if isinstance(result, dict):
        analysis = result.get("structured_response", result.get("output", result))
    else:
        analysis = result
    
    # If result is already the expected model instance, use it directly
    if isinstance(analysis, response_model):
        return analysis
    else:
        # Try to parse from agent output
        return response_model.model_validate(analysis)


def extract_token_usage(result: Any) -> Dict[str, Any]:
    """Extract token usage information from agent response.
    
    Supports:
    - OpenAI/ChatGPT API: input_tokens, output_tokens in response_metadata
    - OpenRouter API: prompt_tokens, completion_tokens, cost in usage object
    
    Args:
        result: Agent invoke result (dict or object)
    
    Returns:
        Dictionary with: input_tokens, output_tokens, total_tokens, model, cost
    """
    default = {"input_tokens": None, "output_tokens": None, "total_tokens": None, "model": None, "cost": None}
    
    def _get(key, default=None):
        return result.get(key, default) if isinstance(result, dict) else getattr(result, key, default)
    
    def _get_from(obj, key, default=None):
        return obj.get(key, default) if isinstance(obj, dict) else getattr(obj, key, default)
    
    try:
        # OpenRouter format: has "usage" key/attribute
        usage = _get("usage")
        if usage:
            input_tokens = _get_from(usage, "prompt_tokens")
            output_tokens = _get_from(usage, "completion_tokens")
            total_tokens = _get_from(usage, "total_tokens")
            return {
                "input_tokens": input_tokens,
                "output_tokens": output_tokens,
                "total_tokens": total_tokens or (input_tokens + output_tokens if input_tokens and output_tokens else None),
                "model": _get("model"),
                "cost": _get_from(usage, "cost")
            }
        
        # OpenAI format: has "response_metadata" or "metadata" key/attribute
        metadata = _get("response_metadata") or _get("metadata")
        if metadata:
            if not isinstance(metadata, dict):
                metadata = {
                    "input_tokens": getattr(metadata, "input_tokens", None),
                    "output_tokens": getattr(metadata, "output_tokens", None),
                    "total_tokens": getattr(metadata, "total_tokens", None),
                    "model": getattr(metadata, "model", None) or getattr(metadata, "model_name", None),
                    "token_usage": getattr(metadata, "token_usage", None)
                }
            
            token_usage = metadata.get("token_usage") or metadata
            input_tokens = _get_from(token_usage, "input_tokens")
            output_tokens = _get_from(token_usage, "output_tokens")
            total_tokens = _get_from(token_usage, "total_tokens")
            return {
                "input_tokens": input_tokens,
                "output_tokens": output_tokens,
                "total_tokens": total_tokens or (input_tokens + output_tokens if input_tokens and output_tokens else None),
                "model": metadata.get("model") or _get("model"),
                "cost": None
            }
    except Exception as e:
        logger.debug(f"Could not extract token usage: {e}")
    
    return default


def load_api(dotenv_dir: Optional[Path] = None, raise_on_missing: bool = False) -> None:
    """
    Load OpenAI API key from .env file and validate it exists.
    
    Args:
        dotenv_dir: Directory containing .env file. If None, load_dotenv searches automatically.
        raise_on_missing: If True, raises ValueError when API key is missing.
    """
    load_dotenv(dotenv_dir / '.env' if dotenv_dir else None)
    
    if not os.getenv('OPENAI_API_KEY'):
        if raise_on_missing:
            raise ValueError("OPENAI_API_KEY not found. Set it in .env file or environment.")
        print("⚠️  WARNING: OPENAI_API_KEY not set!")
        print("This notebook will not work without API access.")
    else:
        print("✅ API key found")

