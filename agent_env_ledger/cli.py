import json
from datetime import datetime
from pathlib import Path

import typer
from rich.console import Console
from rich.table import Table

from agent_env_ledger.scanner import scan_workspace
from agent_env_ledger.scanner import WorkspaceScan

app = typer.Typer(help="Local environment memory for frontier coding agents.")
console = Console()


def _yes_no(value: bool) -> str:
    return "yes" if value else "no"


def _git_dirty_text(value: bool | None) -> str:
    if value is None:
        return "n/a"
    return _yes_no(value)


def _scan_to_dict(result: WorkspaceScan) -> dict[str, object]:
    return {
        "project_path": str(result.project_path),
        "ledger_present": result.ledger_present,
        "git_repo": result.git_repo,
        "git_branch": result.git_branch,
        "git_dirty": result.git_dirty,
        "conda_env": result.conda_env,
        "python_executable": result.python_executable,
        "python_version": result.python_version,
        "platform": result.platform,
        "suggested_test_command": result.suggested_test_command,
    }


def _note_timestamp() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M")


def _append_project_note(ledger_text: str, note_text: str, timestamp: str) -> str:
    note_line = f"- {timestamp}: {note_text}"
    section_heading = "## Project Notes"
    lines = ledger_text.splitlines()

    try:
        section_index = lines.index(section_heading)
    except ValueError:
        if lines and lines[-1] != "":
            lines.append("")
        lines.extend([section_heading, "", note_line])
        return "\n".join(lines) + "\n"

    insert_index = len(lines)
    for index in range(section_index + 1, len(lines)):
        if lines[index].startswith("## "):
            insert_index = index
            break

    lines.insert(insert_index, note_line)
    return "\n".join(lines) + "\n"


def _format_scan_markdown(project: Path) -> str:
    result = scan_workspace(project)

    return "\n".join(
        [
            "---",
            "",
            "## Live Workspace Scan",
            "",
            f"- Project path: {result.project_path}",
            f"- Ledger present: {_yes_no(result.ledger_present)}",
            f"- Git repo: {_yes_no(result.git_repo)}",
            f"- Git branch: {result.git_branch or 'n/a'}",
            f"- Git dirty: {_git_dirty_text(result.git_dirty)}",
            f"- Conda env: {result.conda_env or 'n/a'}",
            f"- Python executable: {result.python_executable}",
            f"- Python version: {result.python_version}",
            f"- Platform: {result.platform}",
            f"- Suggested test command: {result.suggested_test_command or 'n/a'}",
        ]
    )


@app.command()
def init(project: Path = Path.cwd()):
    """Initialize an AGENT_LEDGER.md file in the current project."""
    ledger = project / "AGENT_LEDGER.md"

    if ledger.exists():
        console.print(f"[yellow]Already exists:[/yellow] {ledger}")
        raise typer.Exit(0)

    ledger.write_text(
        """# Agent Ledger

## Project Identity

- Project:
- Purpose:
- Primary Conda environment:
- Default test command:

## Environment Notes

- OS / host:
- Python version:
- GPU / CUDA notes:
- Package manager:

## Safety Rules

- Do not expose secrets.
- Check git status before modifying tracked files.
- Prefer timestamped backups before risky edits.
- Use dry-run modes when available.

## Known Failures and Fixes

| Symptom | Likely Cause | Fix |
|---|---|---|
| | | |

## Last Known Good State

- Date:
- Branch:
- Tests:
- Commit:

## Next Session Handoff

- Completed:
- Current objective:
- Next safe step:
- Open risks:
""",
        encoding="utf-8",
    )

    console.print(f"[green]Created:[/green] {ledger}")


@app.command()
def doctor(project: Path = Path.cwd()):
    """Show basic workspace facts useful to a frontier coding agent."""
    console.print("[bold]Agent Env Ledger Doctor[/bold]")
    console.print(f"Project: {project.resolve()}")
    console.print(f"Ledger present: {(project / 'AGENT_LEDGER.md').exists()}")


@app.command()
def scan(
    project: Path = Path.cwd(),
    json_output: bool = typer.Option(
        False,
        "--json",
        help="Print a compact JSON scan object.",
    ),
):
    """Scan the current workspace and print agent-relevant environment facts."""
    result = scan_workspace(project)

    if json_output:
        typer.echo(json.dumps(_scan_to_dict(result), separators=(",", ":")))
        return

    table = Table(title="Agent Env Ledger Scan")
    table.add_column("Field", style="bold")
    table.add_column("Value")

    table.add_row("Project path", str(result.project_path))
    table.add_row("Ledger present", "yes" if result.ledger_present else "no")
    table.add_row("Git repo", "yes" if result.git_repo else "no")
    table.add_row("Git branch", result.git_branch or "n/a")
    table.add_row("Git dirty", _git_dirty_text(result.git_dirty))

    table.add_row("Conda env", result.conda_env or "n/a")
    table.add_row("Python executable", result.python_executable)
    table.add_row("Python version", result.python_version)
    table.add_row("Platform", result.platform)
    table.add_row("Suggested test command", result.suggested_test_command or "n/a")

    console.print(table)


@app.command()
def note(text: str, project: Path = Path.cwd()):
    """Append a timestamped project note to AGENT_LEDGER.md."""
    ledger = project / "AGENT_LEDGER.md"

    if not ledger.exists():
        console.print("[red]No AGENT_LEDGER.md found. Run:[/red] agent-ledger init")
        raise typer.Exit(1)

    updated = _append_project_note(
        ledger.read_text(encoding="utf-8"),
        text,
        _note_timestamp(),
    )
    ledger.write_text(updated, encoding="utf-8")
    console.print("[green]Note added to AGENT_LEDGER.md[/green]")


@app.command()
def export(
    project: Path = Path.cwd(),
    include_scan: bool = typer.Option(
        False,
        "--include-scan",
        help="Append a read-only live workspace scan in Markdown.",
    ),
):
    """Export a compact handoff brief for a frontier coding agent."""
    ledger = project / "AGENT_LEDGER.md"

    if not ledger.exists():
        console.print("[red]No AGENT_LEDGER.md found. Run:[/red] agent-ledger init")
        raise typer.Exit(1)

    ledger_text = ledger.read_text(encoding="utf-8")

    if not include_scan:
        console.print("[bold]Paste this into your frontier coding agent:[/bold]\n")
        console.print(ledger_text)
        return

    console.print(ledger_text, markup=False)
    console.print()
    console.print(_format_scan_markdown(project), markup=False)


if __name__ == "__main__":
    app()
