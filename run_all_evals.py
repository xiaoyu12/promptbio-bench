#!/usr/bin/env python3
"""Evaluate every task run in an agent's tasks directory against the reference answers.

For each task id found in --runs-dir that also exists in --ref-dir, this calls
run_eval.py as a subprocess:

    python run_eval.py --task-dir   <ref-dir>/<id> \
                       --result-dir <runs-dir>/<id>/output \
                       --output-dir <output-dir> --label <label> --model <model>

Tasks whose <id>_<label>.json already exists with no error are skipped unless
--overwrite is given. When everything has finished, a summary of all per-task
results is written to <output-dir>/summary_<label>.tsv.

Usage:
    python run_all_evals.py                      # ChatGPT subscription via Codex CLI
    python run_all_evals.py --model gpt-5.6      # OpenAI API instead
    python run_all_evals.py --workers 8 --tasks a-6-9,a-1-1
"""

import argparse
import csv
import json
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ROOT = Path(__file__).parent


def _task_ids(runs_dir: Path, ref_dir: Path, only: list[str] | None) -> list[str]:
    ids = sorted(p.name for p in runs_dir.iterdir() if p.is_dir() and not p.name.startswith(("_", ".")))
    if only:
        unknown = set(only) - set(ids)
        if unknown:
            sys.exit(f"❌ Unknown task id(s) in --tasks: {', '.join(sorted(unknown))}")
        ids = [t for t in ids if t in set(only)]
    missing_ref = [t for t in ids if not (ref_dir / t / "eval.json").exists()]
    for t in missing_ref:
        print(f"⚠️  {t}: no eval.json in {ref_dir / t}, skipping")
    return [t for t in ids if t not in missing_ref]


def _already_done(task_id: str, args) -> bool:
    json_path = args.output_dir / f"{task_id}_{args.label}.json"
    if not json_path.exists():
        return False
    try:
        if json.loads(json_path.read_text()).get("error") is not None:
            return False
    except json.JSONDecodeError:
        return False
    # A task can finish with some files scored and others refused for quota; its average
    # covers only part of the files, so it is redone too.
    return not _hit_usage_limit(task_id, args)


USAGE_LIMIT_MARKERS = ("You've hit your usage limit", "You’ve hit your usage limit", "insufficient_quota",
                       "credit_balance_exhausted")


def _hit_usage_limit(task_id: str, args) -> bool:
    """True if this task's eval log shows the LLM backend refusing for quota/credits."""
    for log in (args.output_dir / f"{task_id}_{args.label}.log",
                args.output_dir / "runner_logs" / f"{task_id}_{args.label}.stdout.log"):
        if log.exists() and any(m in log.read_text(errors="replace") for m in USAGE_LIMIT_MARKERS):
            return True
    return False


def _run_one(task_id: str, args) -> tuple[str, int, float]:
    out_dir: Path = args.output_dir
    stdout_path = out_dir / "runner_logs" / f"{task_id}_{args.label}.stdout.log"
    cmd = [
        sys.executable, str(ROOT / "run_eval.py"),
        "--task-dir",   str(args.ref_dir / task_id),
        "--result-dir", str(args.runs_dir / task_id / "output"),
        "--output-dir", str(out_dir),
        "--label",      args.label,
        "--model",      args.model,
    ]
    start = time.time()
    with stdout_path.open("w") as f:
        try:
            rc = subprocess.run(cmd, stdout=f, stderr=subprocess.STDOUT, cwd=ROOT,
                                timeout=args.timeout or None).returncode
        except subprocess.TimeoutExpired:
            f.write(f"\n❌ Timed out after {args.timeout}s\n")
            rc = -1
    return task_id, rc, time.time() - start


def _write_summary(task_ids: list[str], args) -> Path:
    summary_path = args.output_dir / f"summary_{args.label}.tsv"
    rows = []
    for t in task_ids:
        json_path = args.output_dir / f"{t}_{args.label}.json"
        if not json_path.exists():
            rows.append({"task_id": t, "avg_similarity": "", "n_files": "", "n_scored": "", "error": "no result file"})
            continue
        res = json.loads(json_path.read_text())
        files = res.get("files", [])
        rows.append({
            "task_id": t,
            "avg_similarity": "" if res.get("avg_similarity") is None else f"{res['avg_similarity']:.4f}",
            "n_files": len(files),
            "n_scored": sum(f.get("status") in ("success", "invalid") for f in files),
            "error": res.get("error") or "",
        })
    with summary_path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]), delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)

    scores = [float(r["avg_similarity"]) for r in rows if r["avg_similarity"] != ""]
    print(f"\nScored {len(scores)}/{len(rows)} task(s)", end="")
    print(f", mean avg_similarity = {sum(scores) / len(scores):.4f}" if scores else "")
    return summary_path


def main():
    parser = argparse.ArgumentParser(description="Run run_eval.py over all task runs in a directory.")
    parser.add_argument("--runs-dir", type=Path, default=Path("promptbio-bench-claude-skills/tasks"),
                        help="Directory of agent task runs, each with an output/ subdir")
    parser.add_argument("--ref-dir", type=Path, default=Path("promptbio-bench-data/tasks"),
                        help="Directory of reference tasks (task.json, eval.json, ref_answer/)")
    parser.add_argument("--output-dir", type=Path, default=Path("results"))
    parser.add_argument("--label", default="claude-skills")
    parser.add_argument("--model", default="codex:gpt-6.1-sol",
                        help="Eval LLM; 'codex:<model>' uses the ChatGPT subscription via the Codex CLI, "
                             "a bare model name uses the OpenAI API")
    parser.add_argument("--workers", type=int, default=4, help="Number of tasks evaluated in parallel")
    parser.add_argument("--tasks", help="Comma-separated subset of task ids to evaluate")
    parser.add_argument("--timeout", type=int, default=3600, help="Per-task timeout in seconds (0 = none)")
    parser.add_argument("--overwrite", action="store_true", help="Re-run tasks that already have a result")
    args = parser.parse_args()

    only = [t.strip() for t in args.tasks.split(",")] if args.tasks else None
    task_ids = _task_ids(args.runs_dir, args.ref_dir, only)
    (args.output_dir / "runner_logs").mkdir(parents=True, exist_ok=True)

    todo = [t for t in task_ids
            if args.overwrite or not _already_done(t, args)]
    print(f"{len(task_ids)} task(s) found, {len(task_ids) - len(todo)} already done, {len(todo)} to run "
          f"(workers={args.workers}, model={args.model})")

    failed, limited = [], False
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = [pool.submit(_run_one, t, args) for t in todo]
        for i, fut in enumerate(as_completed(futures), 1):
            if fut.cancelled():
                continue
            task_id, rc, elapsed = fut.result()
            status = "ok" if rc == 0 else f"FAILED (rc={rc})"
            if rc != 0:
                failed.append(task_id)
            if _hit_usage_limit(task_id, args):
                status += "  [usage limit]"
                if not limited:
                    limited = True
                    # Every later task would fail the same way; let running ones finish, start no more.
                    n_cancelled = sum(f.cancel() for f in futures)
                    print(f"\n❌ LLM usage limit hit on {task_id}; cancelled {n_cancelled} queued task(s). "
                          f"Re-run the same command once the quota resets to resume.", flush=True)
            print(f"[{i}/{len(todo)}] {task_id}: {status}  {elapsed:.0f}s", flush=True)

    if failed:
        print(f"\n⚠️  {len(failed)} task(s) exited non-zero (see {args.output_dir / 'runner_logs'}): "
              f"{', '.join(sorted(failed))}")

    # Summarise every task, not just a --tasks subset, so the summary is never partial.
    all_ids = _task_ids(args.runs_dir, args.ref_dir, None)
    if all_ids:
        print(f"✅ Summary → {_write_summary(all_ids, args)}")


if __name__ == "__main__":
    main()
