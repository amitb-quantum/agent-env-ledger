# Agent Ledger

## Project Identity

- Project: Agent Env Ledger
- Purpose: Local environment memory and handoff context for frontier coding agents.
- Primary Conda environment: agent-env-ledger
- Default test command: pytest

## Environment Notes

- OS / host: WSL2 Linux development workstation
- Python version: 3.11
- GPU / CUDA notes: not required for this project
- Package manager: Conda + pip editable install

## Safety Rules

- Do not expose secrets or token values.
- Check git status before modifying tracked files.
- Keep first features read-only by default.
- Prefer simple CLI behavior before adding write automation.
- Avoid storing machine-private or employer-specific details in public examples.
- Keep `AGENT_LEDGER.md` human-readable and frontier-model-readable.

## Known Failures and Fixes

| Symptom | Likely Cause | Fix |
|---|---|---|
| `agent-ledger: command not found` | Package not installed into active Conda env | Run `pip install -e .` inside `agent-env-ledger` |
| `Multiple top-level packages discovered` | Setuptools auto-discovery saw `schemas/` and package dir | Configure `[tool.setuptools.packages.find]` in `pyproject.toml` |
| `No such option: --from-scan` | Future command not implemented | Use current commands: `init`, `doctor`, `scan`, `export` |
| `No such option: --write` | Future command not implemented | Keep `scan` read-only for now |

## Last Known Good State

- Date: 2026-06-16
- Branch: main
- Tests: `latest pytest pass after notes feature`
- Commit: latest main includes append-only notes feature
- CLI: `agent-ledger scan`, `agent-ledger scan --json`, `agent-ledger note`, and `agent-ledger export --include-scan` work after `pip install -e .`

## Next Session Handoff

- Completed:
  - Public repo created under `amitb-quantum/agent-env-ledger`
  - Bootstrap README published
  - Secret-like placeholder removed
  - `main` branch configured
  - Bootstrap tag published
  - Read-only `agent-ledger scan` command added
  - Editable install fixed with explicit setuptools package discovery
  - Read-only `agent-ledger export --include-scan` added and tagged as `agent-env-ledger-v0.1.1-scan-export`
  - Machine-readable `agent-ledger scan --json` added and tagged as `agent-env-ledger-v0.1.2-json-scan`
  - Append-only `agent-ledger note` added and tagged as `agent-env-ledger-v0.1.3-notes`
- Current objective:
  - Build the next safe local memory primitive after append-only notes.
- Next safe step:
  - Add `agent-ledger failure add` to record known failures and fixes in the ledger.
- Open risks:
  - Avoid overbuilding write automation too early.
  - Do not store secrets or private machine-specific details.
  - Keep commands read-only unless explicitly named as write operations.

## Project Notes

- 2026-06-17 09:34: First append-only note command added for safe human-authored project memory.
