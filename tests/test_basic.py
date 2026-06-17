import json

from typer.testing import CliRunner

from agent_env_ledger.cli import app

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
