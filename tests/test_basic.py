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
