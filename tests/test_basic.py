import json

from typer.testing import CliRunner

from agent_env_ledger import cli

app = cli.app
runner = CliRunner()


def test_doctor_runs():
    result = runner.invoke(app, ["doctor"])
    assert result.exit_code == 0
    assert "Agent Env Ledger Doctor" in result.output


def test_scan_runs():
    result = runner.invoke(app, ["scan"])
    assert result.exit_code == 0
    assert "Agent Env Ledger Scan" in result.output
    assert "Project path" in result.output
    assert "Python version" in result.output


def test_scan_json_emits_expected_keys(tmp_path):
    result = runner.invoke(app, ["scan", "--project", str(tmp_path), "--json"])

    assert result.exit_code == 0
    data = json.loads(result.output)
    assert set(data) == {
        "project_path",
        "ledger_present",
        "git_repo",
        "git_branch",
        "git_dirty",
        "conda_env",
        "python_executable",
        "python_version",
        "platform",
        "suggested_test_command",
    }
    assert data["project_path"] == str(tmp_path.resolve())
    assert data["ledger_present"] is False
    assert isinstance(data["python_version"], str)


def test_export_default_prints_ledger_only(tmp_path):
    ledger = tmp_path / "AGENT_LEDGER.md"
    ledger.write_text("# Agent Ledger\n\n- Project: test-ledger\n", encoding="utf-8")

    result = runner.invoke(app, ["export", "--project", str(tmp_path)])

    assert result.exit_code == 0
    assert "Paste this into your frontier coding agent:" in result.output
    assert "# Agent Ledger" in result.output
    assert "- Project: test-ledger" in result.output
    assert "Live Workspace Scan" not in result.output
    assert "Python version" not in result.output


def test_export_include_scan_appends_markdown_scan(tmp_path):
    ledger = tmp_path / "AGENT_LEDGER.md"
    ledger.write_text("# Agent Ledger\n\n- Project: test-ledger\n", encoding="utf-8")

    result = runner.invoke(app, ["export", "--project", str(tmp_path), "--include-scan"])

    assert result.exit_code == 0
    assert result.output.startswith("# Agent Ledger")
    assert "- Project: test-ledger" in result.output
    assert "---" in result.output
    assert "## Live Workspace Scan" in result.output
    assert "- Project path:" in result.output
    assert "- Ledger present: yes" in result.output
    assert "- Git repo:" in result.output
    assert "- Python version:" in result.output


def test_note_fails_cleanly_without_ledger(tmp_path):
    result = runner.invoke(app, ["note", "remember this", "--project", str(tmp_path)])

    assert result.exit_code == 1
    assert "No AGENT_LEDGER.md found" in result.output
    assert "agent-ledger init" in result.output


def test_note_creates_project_notes_section(tmp_path, monkeypatch):
    monkeypatch.setattr(cli, "_note_timestamp", lambda: "2026-06-17 09:15")
    ledger = tmp_path / "AGENT_LEDGER.md"
    ledger.write_text("# Agent Ledger\n\n## Project Identity\n\n- Project: test\n", encoding="utf-8")

    result = runner.invoke(app, ["note", "Use dry-run mode.", "--project", str(tmp_path)])

    assert result.exit_code == 0
    assert ledger.read_text(encoding="utf-8") == (
        "# Agent Ledger\n"
        "\n"
        "## Project Identity\n"
        "\n"
        "- Project: test\n"
        "\n"
        "## Project Notes\n"
        "\n"
        "- 2026-06-17 09:15: Use dry-run mode.\n"
    )


def test_note_appends_second_note_without_deleting_first(tmp_path, monkeypatch):
    ledger = tmp_path / "AGENT_LEDGER.md"
    ledger.write_text(
        "# Agent Ledger\n"
        "\n"
        "## Project Notes\n"
        "\n"
        "- 2026-06-17 09:15: First note.\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(cli, "_note_timestamp", lambda: "2026-06-17 10:20")

    result = runner.invoke(app, ["note", "Second note.", "--project", str(tmp_path)])

    assert result.exit_code == 0
    content = ledger.read_text(encoding="utf-8")
    assert "- 2026-06-17 09:15: First note." in content
    assert "- 2026-06-17 10:20: Second note." in content
    assert content.index("First note.") < content.index("Second note.")
