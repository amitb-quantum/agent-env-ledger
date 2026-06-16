from pathlib import Path

import typer
from rich.console import Console
from rich.table import Table

from agent_env_ledger.scanner import scan_workspace

app = typer.Typer(help="Local environment memory for frontier coding agents.")
console = Console()


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
def scan(project: Path = Path.cwd()):
    """Scan the current workspace and print agent-relevant environment facts."""
    result = scan_workspace(project)

    table = Table(title="Agent Env Ledger Scan")
    table.add_column("Field", style="bold")
    table.add_column("Value")

    table.add_row("Project path", str(result.project_path))
    table.add_row("Ledger present", "yes" if result.ledger_present else "no")
    table.add_row("Git repo", "yes" if result.git_repo else "no")
    table.add_row("Git branch", result.git_branch or "n/a")

    if result.git_dirty is None:
        dirty = "n/a"
    else:
        dirty = "yes" if result.git_dirty else "no"
    table.add_row("Git dirty", dirty)

    table.add_row("Conda env", result.conda_env or "n/a")
    table.add_row("Python executable", result.python_executable)
    table.add_row("Python version", result.python_version)
    table.add_row("Platform", result.platform)
    table.add_row("Suggested test command", result.suggested_test_command or "n/a")

    console.print(table)


@app.command()
def export(project: Path = Path.cwd()):
    """Export a compact handoff brief for a frontier coding agent."""
    ledger = project / "AGENT_LEDGER.md"

    if not ledger.exists():
        console.print("[red]No AGENT_LEDGER.md found. Run:[/red] agent-ledger init")
        raise typer.Exit(1)

    console.print("[bold]Paste this into your frontier coding agent:[/bold]\n")
    console.print(ledger.read_text(encoding="utf-8"))


if __name__ == "__main__":
    app()
