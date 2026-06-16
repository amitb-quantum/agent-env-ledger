# Agent Env Ledger

**Local environment memory for frontier coding agents.**

Agent Env Ledger helps frontier coding agents such as ChatGPT, Codex, Claude Code, Cursor, Aider, and other tool-using assistants understand your local development workspace without breaking the isolation that makes your projects safe.

Modern developers often isolate every serious project in its own Conda environment, virtual environment, Docker image, or machine-specific setup. That isolation is good engineering. But frontier models do not automatically understand which environment belongs to which repo, which commands are safe, which failures already happened, which files are protected, or what context should carry across sessions.

Agent Env Ledger solves that problem by creating a compact, local, agent-readable ledger for each project and environment.

It does **not** merge your Conda environments.
It does **not** send your files to a hosted service.
It does **not** store secrets.
It does **not** try to become another agent framework.

Instead, it gives coding agents the missing workspace memory they need before they act.

---

## The Problem

Frontier coding agents are powerful, but every session often starts with amnesia.

They may forget:

* which Conda environment belongs to the current repo
* which Python version is required
* which test command is authoritative
* which branch is safe to modify
* which previous command already failed
* which generated files should not be edited
* which machine-specific constraints matter
* which directories contain important research artifacts
* whether destructive commands require backups or confirmation
* what the previous session had already decided

This creates real daily friction:

> “The agent used the wrong environment again.”

> “It suggested a fix we already tried yesterday.”

> “It edited generated files instead of source files.”

> “It told me to use git on a host where git is not allowed.”

> “It forgot that this project requires dry-run mode.”

> “It wants me to paste an entire prior chat just to continue safely.”

Agent Env Ledger gives the agent a compact continuity layer so it can start with the right project context.

---

## Core Idea

Keep execution isolated. Share only safe context.

A Conda environment should isolate packages, Python versions, CUDA dependencies, compiled libraries, and fragile runtime state.

But frontier models do not need the full environment. They need a small set of stable facts:

* project identity
* environment name
* activation command
* test command
* safety rules
* known failures
* protected paths
* last known good state
* next-session handoff

Agent Env Ledger captures that information locally and exports it as a compact brief that can be pasted into any frontier coding agent.

---

## What Agent Env Ledger Produces

Each project gets an `AGENT_LEDGER.md` file.

Example:

```markdown
# Agent Ledger

## Project Identity

- Project: trident
- Purpose: verified infrastructure-action safety experiments
- Primary Conda environment: trident
- Default test command: pytest

## Environment Notes

- OS / host: WSL Ubuntu
- Python version: 3.11
- Package manager: conda
- GPU / CUDA notes: optional

## Safety Rules

- Do not expose secrets.
- Check git status before modifying tracked files.
- Prefer timestamped backups before risky edits.
- Use dry-run modes when available.
- Do not delete research artifacts unless explicitly instructed.

## Known Failures and Fixes

| Symptom | Likely Cause | Fix |
|---|---|---|
| ModuleNotFoundError | Wrong Conda env active | Activate the project env first |
| Git unavailable | Host policy restriction | Use timestamped backup manifests |

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
```

The ledger is intentionally readable by both humans and frontier models.

---

## Why This Matters

Many tools focus on reducing context size or compressing prompts.

Agent Env Ledger focuses on something different:

**workspace continuity and safe action context.**

It helps prevent coding agents from:

* repeating failed commands
* using the wrong environment
* forgetting project constraints
* losing handoff context
* editing protected files
* taking risky actions without backup awareness
* treating every repo as a generic Python project

This is especially useful for developers who work across many isolated projects, each with its own Conda environment, dependency stack, hardware requirements, and operational rules.

---

## Installation

Clone the repo:

```bash
git clone https://github.com/<your-org-or-user>/agent-env-ledger.git
cd agent-env-ledger
```

Create a Conda environment:

```bash
conda create -n agent-env-ledger python=3.11 -y
conda activate agent-env-ledger
```

Install in editable mode:

```bash
python -m pip install --upgrade pip
pip install -e .
```

Run the CLI:

```bash
agent-ledger doctor
```

---

## Quick Start

Initialize a ledger in your current project:

```bash
cd ~/my-project
agent-ledger init
```

This creates:

```text
AGENT_LEDGER.md
```

Edit the ledger with project-specific facts:

```markdown
- Primary Conda environment: my-project-env
- Default test command: pytest
- Safety rule: do not modify generated files under reports/
```

Export a compact handoff brief:

```bash
agent-ledger export
```

Paste the output into ChatGPT, Codex, Claude Code, Cursor, Aider, or another coding agent before asking it to modify the project.

---

## Example Workflow

A developer has three projects:

```text
~/trident       -> conda activate trident
~/athena2       -> conda activate athena2
~/rosalind      -> conda activate elsd
```

Each project has different rules.

`~/trident` may require tests before commits.

`~/athena2` may require dry-run mode before live actions.

`~/rosalind` may run on a machine where git is unavailable and timestamped backups are preferred.

Instead of explaining this from scratch every session, the developer maintains one ledger per project.

Before using a frontier model:

```bash
cd ~/trident
agent-ledger export
```

The model receives the correct project context before it suggests commands.

---

## What This Is Not

Agent Env Ledger is not:

* a replacement for Conda
* a package manager
* a secrets manager
* an agent runtime
* a hosted memory service
* a prompt compression service
* a vector database
* a model provider
* a CI/CD platform

It is a local context ledger for agent-assisted development.

---

## Safety Principles

Agent Env Ledger is designed around conservative defaults.

### 1. Local-first

Project ledgers live on your machine or inside your repo.

### 2. No secret values

The ledger should never store API keys, tokens, passwords, private keys, or credential values.

It may record that a secret is required, but not the value.

Example:

```yaml
secrets_required:
  OPENAI_API_KEY: required
  GITHUB_TOKEN: optional
```

Never:

```yaml
OPENAI_API_KEY: sk-...
```

### 3. Human-readable

The ledger is plain Markdown so it can be reviewed, edited, copied, diffed, and versioned.

### 4. Agent-readable

The structure is intentionally simple so frontier models can understand it reliably.

### 5. Isolation-preserving

Agent Env Ledger does not combine environments. It only records safe metadata about them.

---

## Planned Features

The first version focuses on a simple local CLI.

Planned capabilities include:

* Conda environment detection
* repo-to-environment mapping
* `conda env export` summarization without noisy dependency dumps
* automatic Python version detection
* git branch and dirty-state summaries
* known failure recording
* safety preflight checks for destructive commands
* protected-path detection
* compact export formats for ChatGPT, Codex, Claude Code, Cursor, and Aider
* MCP server mode for local agent retrieval
* JSON/YAML schema support
* optional machine-level context under `~/.agent-ledger/`

---

## Example Future Commands

```bash
agent-ledger scan
agent-ledger conda map
agent-ledger note "Use dry-run mode before live actions"
agent-ledger failure add
agent-ledger preflight "rm -rf reports/"
agent-ledger export --for codex
agent-ledger export --for claude
agent-ledger mcp serve
```

---

## Why Open Source?

Agent-assisted development is becoming normal, but the local workspace memory layer is still fragile.

Every developer has project-specific context that frontier models need but do not automatically know:

* environment setup
* prior failures
* safe commands
* dangerous paths
* testing expectations
* branch policies
* operational constraints
* handoff notes

Agent Env Ledger aims to make that context explicit, portable, local, and useful.

The goal is simple:

> Help frontier coding agents act less like strangers in your repo.

---

## Project Status

Early prototype.

The first milestone is a working CLI that can:

* initialize `AGENT_LEDGER.md`
* capture basic workspace facts
* export a compact handoff brief
* support human-edited project rules
* run basic tests

Contributions, issues, and real-world workflow examples are welcome.

---

## License

Apache-2.0.
