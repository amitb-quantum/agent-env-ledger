from __future__ import annotations

import os
import platform
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class WorkspaceScan:
    project_path: Path
    ledger_present: bool
    git_repo: bool
    git_branch: str | None
    git_dirty: bool | None
    conda_env: str | None
    python_executable: str
    python_version: str
    platform: str
    suggested_test_command: str | None


def _run_git(project: Path, args: list[str]) -> tuple[int, str, str]:
    proc = subprocess.run(
        ["git", *args],
        cwd=project,
        text=True,
        capture_output=True,
        check=False,
    )
    return proc.returncode, proc.stdout.strip(), proc.stderr.strip()


def _is_git_repo(project: Path) -> bool:
    code, out, _ = _run_git(project, ["rev-parse", "--is-inside-work-tree"])
    return code == 0 and out == "true"


def _git_branch(project: Path) -> str | None:
    code, out, _ = _run_git(project, ["branch", "--show-current"])
    if code != 0 or not out:
        return None
    return out


def _git_dirty(project: Path) -> bool | None:
    code, out, _ = _run_git(project, ["status", "--porcelain"])
    if code != 0:
        return None
    return bool(out)


def _suggest_test_command(project: Path) -> str | None:
    if (project / "pyproject.toml").exists() or (project / "pytest.ini").exists():
        if (project / "tests").exists():
            return "pytest"
    if (project / "package.json").exists():
        return "npm test"
    if (project / "Makefile").exists():
        return "make test"
    return None


def scan_workspace(project: Path) -> WorkspaceScan:
    project = project.resolve()
    git_repo = _is_git_repo(project)

    return WorkspaceScan(
        project_path=project,
        ledger_present=(project / "AGENT_LEDGER.md").exists(),
        git_repo=git_repo,
        git_branch=_git_branch(project) if git_repo else None,
        git_dirty=_git_dirty(project) if git_repo else None,
        conda_env=os.environ.get("CONDA_DEFAULT_ENV"),
        python_executable=sys.executable,
        python_version=platform.python_version(),
        platform=platform.platform(),
        suggested_test_command=_suggest_test_command(project),
    )
