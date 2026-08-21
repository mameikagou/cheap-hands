#!/usr/bin/env python3
"""Run DSH in a caller-selected workspace and retain before/after review evidence."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import re
import shlex
import shutil
import subprocess
import sys
import tempfile
from typing import Any, Sequence


DEFAULT_MODEL = "stealth/ox-alpha"
DEFAULT_TIMEOUT_SECONDS = 1800
ORI_PLUGIN_PACKAGE = "@openrouter/dsh-ori-openrouter"


class RunnerError(RuntimeError):
    """A user-correctable preflight or runner error."""


def command_path(command: str) -> str | None:
    """Resolve one executable without invoking a shell."""
    if os.sep in command:
        path = Path(command).expanduser().resolve()
        return str(path) if path.is_file() and os.access(path, os.X_OK) else None
    return shutil.which(command)


def run_process(
    args: Sequence[str],
    *,
    cwd: Path,
    env: dict[str, str] | None = None,
    timeout: int | None = None,
) -> subprocess.CompletedProcess[str]:
    """Run an argv vector with captured UTF-8 text output."""
    return subprocess.run(
        list(args),
        cwd=cwd,
        env=env,
        text=True,
        encoding="utf-8",
        errors="replace",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=timeout,
        check=False,
    )


def git(repo: Path, *args: str) -> subprocess.CompletedProcess[str]:
    """Run Git at the owning repository root."""
    return run_process(["git", "-C", str(repo), *args], cwd=repo)


def resolve_workspace(workspace_arg: str) -> tuple[Path, Path]:
    """Return the exact selected directory and its owning Git root."""
    workspace = Path(workspace_arg).expanduser().resolve()
    if not workspace.is_dir():
        raise RunnerError(f"workspace directory does not exist: {workspace}")
    probe = run_process(["git", "-C", str(workspace), "rev-parse", "--show-toplevel"], cwd=workspace)
    if probe.returncode != 0:
        raise RunnerError(f"not inside a Git workspace: {workspace}\n{probe.stderr.strip()}")
    return workspace, Path(probe.stdout.strip()).resolve()


def repository_state(workspace: Path, repo: Path, dsh_bin: str, ori_bin: str) -> dict[str, Any]:
    """Return machine-readable prerequisites and current source state."""
    status = git(repo, "status", "--porcelain=v1", "--untracked-files=all")
    head = git(repo, "rev-parse", "HEAD")
    if status.returncode != 0 or head.returncode != 0:
        raise RunnerError((status.stderr or head.stderr).strip())
    dirty_lines = [line for line in status.stdout.splitlines() if line]
    return {
        "workspace": str(workspace),
        "repo": str(repo),
        "head": head.stdout.strip(),
        "clean": not dirty_lines,
        "dirty_entries": dirty_lines,
        "dsh": command_path(dsh_bin),
        "ori": command_path(ori_bin),
        **dsh_configuration_state(DEFAULT_MODEL),
        "notes": [
            "DSH runs directly in the selected workspace.",
            "This plugin never creates, switches, removes, or prunes Git worktrees.",
            "DSH read and network access depend on local DSH policy.",
        ],
    }


def harness_home() -> Path:
    """Return DSH's configured home without reading credential contents."""
    return Path(os.environ.get("DSH_HOME", "~/.dsh")).expanduser().resolve()


def model_in_catalog(settings: Path, model: str) -> bool:
    """Check the value-free DSH settings document for one catalog model id."""
    try:
        text = settings.read_text(encoding="utf-8")
    except OSError:
        return False
    pattern = rf"^\s*-\s+id:\s*['\"]?{re.escape(model)}['\"]?\s*$"
    return re.search(pattern, text, flags=re.MULTILINE) is not None


def dsh_configuration_state(model: str) -> dict[str, Any]:
    """Report local, non-secret OpenRouter/headless configuration evidence."""
    home = harness_home()
    settings = home / "settings.yaml"
    package_json = home / "profiles" / "headless" / "package.json"
    plugin_installed = False
    try:
        package = json.loads(package_json.read_text(encoding="utf-8"))
        plugin_installed = ORI_PLUGIN_PACKAGE in package.get("dependencies", {})
    except (OSError, ValueError, TypeError):
        pass
    return {
        "dsh_home": str(home),
        "model_present_in_catalog": model_in_catalog(settings, model),
        "headless_openrouter_plugin_installed": plugin_installed,
    }


def worker_prompt(task: str) -> str:
    """Add fixed handoff requirements around the scoped task."""
    return f"""You are an implementation worker. Work directly in the current workspace selected by the reviewing Codex agent.

Task from the reviewing Codex agent:
{task.strip()}

Constraints:
- Inspect the repository instructions before editing.
- Do not create, remove, switch, or prune Git worktrees.
- Do not commit, create branches, alter Git remotes, reset, revert, clean, or stash changes.
- Do not read credential files, `.env` files, production data, or paths outside this workspace.
- Preserve pre-existing edits and avoid unrelated cleanup.
- Keep changes within the requested scope and run relevant deterministic checks when possible.
- Finish with: summary, changed files, checks actually run, and remaining risks.
"""


def write_text(path: Path, value: str) -> None:
    """Write one UTF-8 review artifact."""
    path.write_text(value, encoding="utf-8")


def untracked_files(repo: Path) -> list[str]:
    """List untracked, non-ignored files without changing the index."""
    result = git(repo, "ls-files", "--others", "--exclude-standard", "-z")
    if result.returncode != 0:
        raise RunnerError(result.stderr.strip())
    return [item for item in result.stdout.split("\0") if item]


def untracked_patch(repo: Path, paths: list[str]) -> str:
    """Render new files into a binary-capable patch without `git add`."""
    chunks: list[str] = []
    for relative in paths:
        result = git(repo, "diff", "--binary", "--no-index", "--", "/dev/null", relative)
        if result.returncode not in (0, 1):
            chunks.append(result.stderr)
        else:
            chunks.append(result.stdout)
    return "".join(chunks)


def collect_state(repo: Path, bundle: Path, prefix: str) -> dict[str, Any]:
    """Capture Git status and a patch without mutating the workspace or index."""
    status = git(repo, "status", "--short", "--untracked-files=all")
    tracked_patch = git(repo, "diff", "--binary", "--no-ext-diff", "HEAD", "--")
    diff_check = git(repo, "diff", "--check", "HEAD", "--")
    names = git(repo, "diff", "--name-only", "HEAD", "--")
    new_files = untracked_files(repo)
    patch_text = tracked_patch.stdout + tracked_patch.stderr + untracked_patch(repo, new_files)
    changed_files = sorted(set([line for line in names.stdout.splitlines() if line] + new_files))
    write_text(bundle / f"{prefix}-status.txt", status.stdout + status.stderr)
    write_text(bundle / f"{prefix}.patch", patch_text)
    write_text(bundle / f"{prefix}-diff-check.txt", diff_check.stdout + diff_check.stderr)
    return {
        "changed_files": changed_files,
        "git_status_exit": status.returncode,
        "git_diff_exit": tracked_patch.returncode,
        "git_diff_check_exit": diff_check.returncode,
    }


def preflight(args: argparse.Namespace) -> int:
    """Print prerequisites without mutating workspace or configuration state."""
    try:
        workspace, repo = resolve_workspace(args.workspace)
        result = repository_state(workspace, repo, args.dsh_bin, args.ori_bin)
    except RunnerError as error:
        print(json.dumps({"ok": False, "error": str(error)}, indent=2), file=sys.stderr)
        return 2
    result["ok"] = result["dsh"] is not None
    result["requested_model"] = args.model
    result.update(dsh_configuration_state(args.model))
    print(json.dumps(result, indent=2))
    return 0 if result["ok"] else 3


def configure_with_ori(
    workspace: Path, ori_bin: str, dsh_bin: str, model: str
) -> subprocess.CompletedProcess[str]:
    """Configure Ori plus the DSH headless profile used by this runner."""
    resolved = command_path(ori_bin)
    if resolved is None:
        raise RunnerError("Ori is not installed or executable; configure DSH directly or install Ori with authorization")
    dsh_resolved = command_path(dsh_bin)
    if dsh_resolved is None:
        raise RunnerError("dsh is not installed or executable")
    env = os.environ.copy()
    env["ORI_TELEMETRY"] = "0"
    env["DSH_TELEMETRY_DISABLED"] = "1"
    outputs: list[str] = []
    errors: list[str] = []

    def step(argv: list[str], *, timeout: int = 120) -> subprocess.CompletedProcess[str]:
        result = run_process(argv, cwd=workspace, env=env, timeout=timeout)
        outputs.append(result.stdout)
        errors.append(result.stderr)
        return result

    ori_result = step([resolved, "dsh", "--model", model])
    if ori_result.returncode != 0:
        return subprocess.CompletedProcess(ori_result.args, ori_result.returncode, "".join(outputs), "".join(errors))

    # Ori initializes web. The review runner uses headless, so initialize it
    # and install the exact Ori-provided plugin there as well.
    init_result = step([dsh_resolved, "--profile", "headless", "--help"])
    if init_result.returncode != 0:
        return subprocess.CompletedProcess(init_result.args, init_result.returncode, "".join(outputs), "".join(errors))
    plugin_archive = harness_home() / "ori" / "ori-dsh-plugin.tgz"
    if not plugin_archive.is_file():
        errors.append(f"Ori plugin archive is missing: {plugin_archive}\n")
        return subprocess.CompletedProcess([], 1, "".join(outputs), "".join(errors))
    install_result = step(
        [dsh_resolved, "plugin", "--profile", "headless", "add", f"file:{plugin_archive}"]
    )
    if install_result.returncode != 0:
        return subprocess.CompletedProcess(install_result.args, install_result.returncode, "".join(outputs), "".join(errors))

    # The Ori plugin refreshes the per-user catalog asynchronously. A cold
    # headless one-shot validates its model before that refresh finishes, so
    # briefly boot web when the requested id is not cached yet.
    settings = harness_home() / "settings.yaml"
    if not model_in_catalog(settings, model):
        try:
            step([dsh_resolved, "web", "--host", "127.0.0.1", "--port", "0"], timeout=12)
        except subprocess.TimeoutExpired as error:
            outputs.append(error.stdout or "")
            errors.append(error.stderr or "")
        if not model_in_catalog(settings, model):
            errors.append(f"OpenRouter catalog did not expose requested model {model!r}\n")
            return subprocess.CompletedProcess([], 1, "".join(outputs), "".join(errors))
    return subprocess.CompletedProcess([], 0, "".join(outputs), "".join(errors))


def run_worker(args: argparse.Namespace) -> int:
    """Invoke DSH once in place and retain before/after review files."""
    try:
        workspace, repo = resolve_workspace(args.workspace)
        state = repository_state(workspace, repo, args.dsh_bin, args.ori_bin)
        dsh_path = command_path(args.dsh_bin)
        if dsh_path is None:
            raise RunnerError("dsh is not installed or executable; run preflight and follow the setup reference")
    except RunnerError as error:
        print(json.dumps({"ok": False, "error": str(error)}, indent=2), file=sys.stderr)
        return 2

    bundle = Path(tempfile.mkdtemp(prefix="dsh-worker-review-"))
    prompt = worker_prompt(args.task)
    write_text(bundle / "task.txt", prompt)
    before = collect_state(repo, bundle, "before")

    setup_result: subprocess.CompletedProcess[str] | None = None
    if args.configure_with_ori:
        try:
            setup_result = configure_with_ori(workspace, args.ori_bin, dsh_path, args.model)
        except RunnerError as error:
            write_text(bundle / "setup-error.txt", str(error) + "\n")
            print(json.dumps({"ok": False, "error": str(error), "bundle": str(bundle)}, indent=2), file=sys.stderr)
            return 4
        write_text(bundle / "ori-output.txt", setup_result.stdout)
        write_text(bundle / "ori-error.txt", setup_result.stderr)
        if setup_result.returncode != 0:
            print(
                json.dumps(
                    {"ok": False, "error": "Ori could not configure DSH", "bundle": str(bundle), "ori_exit": setup_result.returncode},
                    indent=2,
                ),
                file=sys.stderr,
            )
            return 4

    env = os.environ.copy()
    env["DSH_PERMISSION_MODE"] = "workspace-write"
    env["DSH_TELEMETRY_DISABLED"] = "1"
    timed_out = False
    try:
        worker = run_process(
            [dsh_path, "--profile", "headless", prompt],
            cwd=workspace,
            env=env,
            timeout=args.timeout,
        )
        worker_exit = worker.returncode
        worker_stdout = worker.stdout
        worker_stderr = worker.stderr
    except subprocess.TimeoutExpired as error:
        timed_out = True
        worker_exit = 124
        worker_stdout = error.stdout or ""
        worker_stderr = (error.stderr or "") + f"\nDSH worker timed out after {args.timeout} seconds.\n"

    write_text(bundle / "worker-output.txt", worker_stdout)
    write_text(bundle / "worker-error.txt", worker_stderr)
    after = collect_state(repo, bundle, "after")
    configuration = dsh_configuration_state(args.model)
    manifest = {
        "version": 2,
        "ok": worker_exit == 0 and after["git_diff_check_exit"] == 0,
        "workspace": str(workspace),
        "repo": str(repo),
        "base_commit": state["head"],
        "bundle": str(bundle),
        "requested_model": args.model,
        "model_configured_in_this_run": bool(args.configure_with_ori and setup_result and setup_result.returncode == 0),
        **configuration,
        "workspace_was_clean": state["clean"],
        "worker_command": shlex.join([dsh_path, "--profile", "headless", "<task from task.txt>"]),
        "worker_exit": worker_exit,
        "timed_out": timed_out,
        "permission_mode": env["DSH_PERMISSION_MODE"],
        "telemetry_disabled": True,
        "changed_files_before": before["changed_files"],
        "changed_files_after": after["changed_files"],
        "git_diff_check_exit": after["git_diff_check_exit"],
    }
    write_text(bundle / "manifest.json", json.dumps(manifest, indent=2) + "\n")
    print(json.dumps(manifest, indent=2))
    return 0 if manifest["ok"] else min(max(worker_exit, 1), 125)


def parser() -> argparse.ArgumentParser:
    """Build the command-line parser."""
    root = argparse.ArgumentParser(description=__doc__)
    subcommands = root.add_subparsers(dest="command", required=True)

    def common(target: argparse.ArgumentParser) -> None:
        target.add_argument("--workspace", default=".", help="Exact directory where DSH must run")
        target.add_argument("--model", default=DEFAULT_MODEL, help="Expected OpenRouter model identifier")
        target.add_argument("--dsh-bin", default=os.environ.get("DSH_BIN", "dsh"), help="DSH executable name or path")
        target.add_argument("--ori-bin", default=os.environ.get("ORI_BIN", "ori"), help="Optional Ori executable name or path")

    check = subcommands.add_parser("preflight", help="Check Git, DSH, Ori, and workspace state")
    common(check)
    check.set_defaults(handler=preflight)

    execute = subcommands.add_parser("run", help="Run one DSH implementation task in place")
    common(execute)
    execute.add_argument("--task", required=True, help="Scoped implementation task and acceptance criteria")
    execute.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT_SECONDS, help="Worker timeout in seconds")
    execute.add_argument(
        "--configure-with-ori",
        action="store_true",
        help="Run `ori dsh --model ...` first; this optional action mutates global DSH configuration",
    )
    execute.set_defaults(handler=run_worker)
    return root


def main() -> int:
    """CLI entry point."""
    args = parser().parse_args()
    if getattr(args, "timeout", 1) <= 0:
        print(json.dumps({"ok": False, "error": "--timeout must be positive"}, indent=2), file=sys.stderr)
        return 2
    return int(args.handler(args))


if __name__ == "__main__":
    raise SystemExit(main())
