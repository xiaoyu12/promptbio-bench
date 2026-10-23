# Genearl LLM Agent Results for Promptbio-Bench

[![Website](https://img.shields.io/badge/Website-promptbio-blue?style=flat-square)](https://promptbio.github.io/promptbio-bench) [![Code](https://img.shields.io/badge/Code-GitHub-black?style=flat-square&logo=github)](https://github.com/promptbio/promptbio-bench) [![Preprint](https://img.shields.io/badge/Preprint-bioRxiv-b31b1b?style=flat-square)](https://doi.org/10.64898/2026.05.05.723092) [![Data](https://img.shields.io/badge/Data-HuggingFace-yellow?style=flat-square&logo=huggingface)](https://huggingface.co/datasets/promptbio-ai/promptbio-bench-data)

This repository contains the updated evaluation framework for [PromptBio-bench](https://doi.org/10.64898/2026.05.05.723092), a benchmark of 244 tasks spanning bioinformatics and data science. Given a task and an agent output directory, it runs a 4-step LLM-assisted pipeline to score how well the output matches the reference answer.

<p align="center">
  <img src="docs/img/promptbio-bench.png" alt="PromptBio-bench overview: task datasets spanning genomics, epigenomics, transcriptomics, proteomics, metabolomics, metagenomics, single-cell omics, and data science / statistics / ML; each task pairs a description, input data, and reference answer; an agent consumes the task and produces result files, which are scored by the Match → Detect → Recommend → Compare pipeline." width="900">
</p>

--- 

## Prerequisites

- Conda (Miniconda or Miniforge3)
- One LLM backend for the evaluator (see [Choosing the evaluator LLM](#choosing-the-evaluator-llm)):
  - an OpenAI API key (`OPENAI_API_KEY`), or
  - the [Codex CLI](https://github.com/openai/codex), logged in with a ChatGPT subscription, or
  - the [Claude Code CLI](https://code.claude.com/docs), logged in with a Claude subscription

## Quick start

### 1) Create and activate the environment

```bash
conda env create -f environment.yml
conda activate bench
```

### 2) Set up an LLM backend

Pick one:

```bash
# OpenAI API: key loaded from .env by utils/agents.py (python-dotenv)
echo "OPENAI_API_KEY=sk-..." > .env

# Codex CLI (ChatGPT subscription), used with --model codex:<model>
codex login

# Claude Code CLI (Claude subscription), used with --model claude:<model>
claude   # log in once interactively, then exit
```

### 3) Run an evaluation

Single agent:

```bash
python run_eval.py \
  --task-dir   <path/to/task> \
  --result-dir <path/to/agent/output> \
  --output-dir <path/to/save/results> \
  --label      <agent_name> \
  --model      codex:gpt-6.1-sol
```

Multiple agents (Steps 2 & 3 run only once):

```bash
python run_eval.py \
  --task-dir   <path/to/task> \
  --result-dir <path/to/agent1>,<path/to/agent2>,<path/to/agent3> \
  --label      agent1,agent2,agent3 \
  --output-dir <path/to/save/results>
```

### 4) Evaluate a whole agent run

`run_all_evals.py` calls `run_eval.py` for every task an agent attempted and writes a summary:

```bash
python run_all_evals.py \
  --runs-dir   <agent-run>/tasks \
  --ref-dir    promptbio-bench-data/tasks \
  --output-dir <path/to/save/results> \
  --label      <agent_name> \
  --model      claude:claude-opus-5-5 \
  --workers    4
```

`--runs-dir` holds one folder per task id, each with an `output/` subfolder containing the agent's files. Tasks are evaluated in parallel (`--workers`). The run can be stopped and restarted:

- Tasks that already have an error-free result are skipped (`--overwrite` re-runs them).
- `--tasks a-1-1,b-7-4` limits the run to a subset; the summary always covers every task.
- When the backend reports a usage or credit limit (ChatGPT, Claude or OpenAI), queued tasks are cancelled, so a limit costs at most the tasks in flight. Re-run the same command after the reset; tasks whose log shows a limit error are redone, including ones that were only partly scored.

When everything has finished, `<output-dir>/summary_<label>.tsv` lists each task's `avg_similarity`, number of files and number scored, and any error.

---

## CLI reference

### `run_eval.py` arguments

| Argument | Required | Description |
|---|---|---|
| `--task-dir` | yes | Task directory containing `task.json`, `eval.json`, and `ref_answer/` |
| `--result-dir` | yes | Comma-separated agent result directories to evaluate |
| `--output-dir` | yes | Directory where comparison results and logs will be saved |
| `--label` | no | Comma-separated labels for output filenames, one per `--result-dir` (default: `agent`). If a single label is given for multiple result dirs, it is auto-suffixed with `_0`, `_1`, … |
| `--model` | no | LLM for matching, format detection, strategy recommendation, and comparison (default: `codex:gpt-5.6-sol`) |

### `run_all_evals.py` arguments

| Argument | Default | Description |
|---|---|---|
| `--runs-dir` | `promptbio-bench-claude-skills/tasks` | Agent run: one folder per task, each with an `output/` subfolder |
| `--ref-dir` | `promptbio-bench-data/tasks` | Reference tasks (`task.json`, `eval.json`, `ref_answer/`) |
| `--output-dir` | `results` | Where per-task results, logs and the summary are written |
| `--label` | `claude-skills` | Label used in output file names |
| `--model` | `codex:gpt-6.1-sol` | Evaluator LLM (see below) |
| `--workers` | `4` | Tasks evaluated in parallel |
| `--tasks` | all | Comma-separated subset of task ids |
| `--timeout` | `3600` | Per-task evaluation timeout in seconds (`0` = none) |
| `--overwrite` | off | Re-run tasks that already have a result |

### Choosing the evaluator LLM

The `--model` value selects both the model and how it is reached:

| `--model` | Backend | Billing |
|---|---|---|
| `gpt-5.6`, `gpt-6.1`, … | OpenAI API via LangChain | API key (`OPENAI_API_KEY`) |
| `codex:gpt-6.1-sol`, `codex:gpt-5.6-sol`, … | `codex exec` (Codex CLI), read-only sandbox | ChatGPT subscription |
| `claude:claude-opus-5-5`, … | `claude -p` (Claude Code CLI) with no tools, MCP servers or settings files | Claude subscription |

The CLI backends treat the model as a plain judge: images are passed as images, and structured answers are validated against the expected JSON schema and retried up to three times. Every step of the pipeline uses the selected model. Optional environment variables:

| Variable | Effect |
|---|---|
| `CODEX_TIMEOUT`, `CLAUDE_TIMEOUT` | Per-call timeout in seconds (default 900) |
| `CODEX_REASONING_EFFORT` | `model_reasoning_effort` passed to Codex |
| `CLAUDE_EFFORT` | `--effort` passed to Claude Code (`low` … `max`) |

### Output files

One set of files per agent is saved to `--output-dir`:

| File | Description |
|---|---|
| `<task_id>_<label>.log` | Full pipeline log |
| `<task_id>_<label>.json` | Per-file similarity scores and status |
| `<task_id>_<label>_full.json` | Full intermediate state for debugging |
| `summary_<label>.tsv` | Per-task summary (written by `run_all_evals.py`) |

--- 

## Pipeline overview

Each evaluation runs four steps:

1. **Match** — LLM maps agent output files to reference files. *(per agent)*
2. **Detect** — identify the format of each reference file. *(shared — runs once)*
3. **Recommend** — LLM chooses comparison strategy + parameters per file. *(shared — runs once)*
4. **Compare** — compute similarity (0–1) for each file pair. *(per agent)*

Steps 2 and 3 only look at the reference files and the question — never at
agent output — so their results are valid for every agent. When multiple
`--result-dir` paths are supplied, they run once and are reused for each
agent's Match/Compare pass, reducing cost and latency.

Final score is the average similarity across all scored reference files. A task counts as accurate when its score is at least 0.5.

## Task data and directory structure

Tasks can be downloaded from Hugging Face: [promptbio-ai/promptbio-bench-data](https://huggingface.co/datasets/promptbio-ai/promptbio-bench-data).

Each task is stored in a directory named by its task ID. The directory (passed via `--task-dir`) should look like:

```text
<task-dir>/
├── task.json        # Task definition shown to the agent
├── eval.json        # Evaluation spec used by run_eval.py
├── ref_answer/      # Reference output files
│   └── A375_WGS_WMG.cnv.vcf.gz.tbi
├── ref_script/      # Reference solution scripts (not used by evaluator)
│   └── work.sh
└── data/            # Input files provided to the agent (optional)
    └── A375_WGS_WMG.cnv.vcf.gz
```

### `task.json` example

```json
{
  "id": "a-1-2",
  "question": "Please generate a tabix index for the provided VCF.gz file.",
  "input_files": ["data/A375_WGS_WMG.cnv.vcf.gz"],
  "expected_output": [
    {"file": "A375_WGS_WMG.cnv.vcf.gz.tbi", "type": "tbi", "description": ""}
  ],
  "timeout_seconds": 3600
}
```

### `eval.json` example

```json
{
  "id": "a-1-2",
  "question": "Please generate a tabix index for the provided VCF.gz file.",
  "ref_answer": ["ref_answer/A375_WGS_WMG.cnv.vcf.gz.tbi"],
  "ref_script": ["ref_script/work.sh"],
  "scoring": {
    "expected_output": [
      {
        "file": "A375_WGS_WMG.cnv.vcf.gz.tbi",
        "guidelines": "The file must be a valid tabix index for the input VCF.gz file; internal byte layout may differ."
      }
    ]
  }
}
```

`ref_answer` paths are relative to `--task-dir`. Optional `guidelines` give the LLM hints about strictness for that file.

## Supported formats and strategies

Each reference file is routed to a handler in `tools/` (registered in `tools/factory.py`). Step 3 picks a comparison **strategy** and parameters from [`tools/tool_schema.json`](tools/tool_schema.json).

| Schema key | Extensions | Default strategy | Other strategies |
|---|---|---|---|
| `fasta` | `.fasta`, `.fa` | exact | approximate, summary |
| `fastq` | `.fastq`, `.fq` | exact | approximate, summary |
| `bam` | `.bam`, `.sam`, `.cram` | summary | exact, approximate, coverage, variant |
| `bai` | `.bai`, `.crai` | functional | summary |
| `tbi` | `.tbi`, `.csi` | functional | summary |
| `fai` | `.fai` | exact | approximate, summary |
| `vcf` | `.vcf`, `.vcf.gz`, `.bcf` | summary | exact, approximate |
| `bed` | `.bed`, `.bedgraph`, `.bg`, `.bigbed` | approximate | exact, overlap, correlation, summary |
| `bigwig` | `.bw`, `.bigwig`, `.wig` | summary | exact, approximate, correlation |
| `table` | `.csv`, `.tsv`, `.gct`, `.table`, `.xlsx` | approximate | exact, summary, semantic |
| `pdb` | `.pdb`, `.cif`, `.mmcif` | exact | approximate, summary |
| `image` | `.png`, `.jpg`, `.pdf`, `.svg`, … | semantic | — |
| `txt` | `.txt`, `.text` | semantic | exact, approximate, numeric, summary |

For tables, the comparison plan scores each value column with `exact`, `overlap`, `rae`, `pearson`, `spearman` or `partition`. `partition` scores cluster or module labels after the best one-to-one relabelling. A numeric column can set `compare_abs` when its sign is only a convention the task leaves open, such as a ppm error defined as observed − theoretical or the reverse. A text file holding a single number is always compared with `numeric`. A guideline tolerance of "N-fold" or "k orders of magnitude" becomes a relative tolerance of N − 1 (99 for two orders of magnitude), which sets no lower bound for positive values.

## Evaluator fixes

A failure analysis of agent runs found scoring errors that gave correct answers low scores. They are fixed in this version. All fixes are task-independent and apply to every agent:

| Area | Before | Now |
|---|---|---|
| Tables whose only columns are row keys, or whose value columns are all ignored or unscorable | Score 0 | F1 of matched row keys (or of whole rows when rows are not keyed) |
| Reference and candidate both empty (header only) | Candidate marked invalid, score 0 | Score 1.0 |
| Boolean columns | `astype(bool)` turned "No" into `True` | Explicit yes/no/true/false mapping |
| Small result tables (≤ 100 cells) under `summary` | Scored on shape and value distributions | Compared value by value (`approximate`) |
| FASTQ reads with renamed IDs | Matched by read name only | Fall back to identical sequence + quality |
| FASTA `by_name` with no shared IDs | Score 0 | Fall back to matching by sequence |
| Text `ignore_whitespace` | Deleted newlines, breaking line-by-line comparison | Keeps line structure |
| Numeric text tolerance | Checked against a similarity capped at 1, so any tolerance ≥ 1 passed every value | Checked against the raw relative error |
| Pearson columns | `pearsonr(nan_policy=…)` is unsupported on older SciPy, so every Pearson score was 0 | NaN policy applied before the call |
| Format detection | Ignored `--model` and called a hard-coded API model | Uses the run's model (exported as `EVAL_MODEL`) |
| Row keys | Exact string match only | Normalised (case, separators, integral floats), one-sided prefixes/suffixes stripped when that increases matches, float keys compared at the reference's precision |
| Table parsing | `#` lines after the data were parsed as rows; a delimiter spelled `\t` by the LLM disabled quote handling | Trailing comment lines dropped; delimiters normalised |
| Image judge | Mirrored axes or a different colormap read as different data | Prompt treats axis direction, 0- vs 1-based indices and colormaps as presentation choices |

Note that the specialist-agent scores in the PromptBio-Bench preprint were produced before these fixes.

## Results in this repository

Scores for two Claude Opus 5.5 runs (Claude Code at high effort, one subagent per task), with and without 667 bioinformatics Agent Skills:

| Folder | Agent run | Evaluator | Judge model |
|---|---|---|---|
| `claude-skills/` | with skills | original | GPT-5.6 (API) and GPT-5.6-sol |
| `claude-skills-claude-judge/` | with skills | fixed | `claude:claude-opus-5-5` |
| `claude-no-skills-claude-judge/` | without skills | fixed | `claude:claude-opus-5-5` |
| `claude-no-skills/` | without skills | original (first attempt, superseded) | GPT-5.6-sol |

`site/data/results.csv` holds the original-evaluator scores of all agents shown on the website. `.log` files and `runner_logs/` are not tracked.

## Troubleshooting

- **Missing API key:** ensure `.env` contains `OPENAI_API_KEY`, or use a `codex:` or `claude:` model instead.
- **`codex exec failed` / `claude -p failed`:** check that the CLI is installed and logged in (`codex login`, or run `claude` once). Usage-limit messages mean the subscription quota is exhausted; `run_all_evals.py` stops queuing tasks and can be re-run after the reset.
- **Command-line tool errors** (`samtools`, `bcftools`, `tabix`, `sort-bed`): verify `conda activate bench` and tool availability in PATH.
- **Handler mismatch or unknown format:** check `tools/tool_schema.json`, `tools/factory.py`, and the file's extension and content.


## Project structure

```text
run_eval.py              # CLI entrypoint: evaluate one task for one or more agents
run_all_evals.py         # Evaluate every task of an agent run; resumable, writes a summary
utils/                   # Match, format detection, strategy, compare, LLM backends (agents.py)
tools/                   # Format handlers + tool_schema.json
analysis/                # Dashboard data preparation
site/                    # Project website and results data
environment.yml          # Conda environment (Python deps + CLI tools)
```

## License

Licensed under the [Apache License 2.0](LICENSE).
