# LordCoder

LordCoder is now a native, cross-platform, local-first coding core. Phase 1 provides an installable Python package, a real `lordcoder` CLI, a localhost REST API, policy-gated file writes and shell execution, and a compatibility layer for the older `lordcoder.yml` / `.lordcoder-model` workflow.

Primary phase-1 commands:

- `lordcoder init`
- `lordcoder doctor`
- `lordcoder daemon`
- `lordcoder plan`
- `lordcoder apply`
- `lordcoder test`
- `lordcoder version`

Primary API routes:

- `GET /healthz`
- `POST /v1/plan`
- `POST /v1/apply`
- `POST /v1/test`

## Features

- Multi-file coding assistance through Aider
- Persisted model selection on first launch
- Support for any Aider-compatible model string
- Ollama-aware startup checks only when using `ollama/...` models
- Auto-commit, git, and pytest settings baked into the base config

## Quick Start

### Prerequisites

- Python 3.8+
- Windows 10/11
- Ollama only if you plan to use an `ollama/...` model
- Enough RAM for the model you choose

### Install

Recommended:

```bash
pip install .
```

Initialize a project config:

```bash
lordcoder init
```

Run diagnostics:

```bash
lordcoder doctor
lordcoder doctor --json
lordcoder doctor --recommend-model
```

Start the daemon:

```bash
lordcoder daemon
```

If you want local Ollama models, install Ollama from <https://ollama.com>. `lordcoder doctor` will tell you whether the runtime is reachable and which model size is a safer fit for the current machine.

### Launch

Primary product entrypoint:

```bash
lordcoder --version
```

Legacy Windows launchers are still present in the repo as compatibility helpers, but they are no longer the main runtime path.

## Model Selection

On first launch, LordCoder prompts you to select a model. The current built-in presets are:

- `ollama/qwen2.5-coder:7b`
- `ollama/qwen2.5-coder:14b`
- `ollama/qwen2.5-coder:32b`

You can also enter any custom Aider-compatible model string, such as `openai/gpt-5` or `anthropic/claude-3-7-sonnet`.

LordCoder saves your choice in `.lordcoder-model` and generates `lordcoder.effective.yml` from the checked-in `lordcoder.yml`.

## Project Files

- `lordcoder.yml`: base config committed to the repo
- `lordcoder.effective.yml`: generated runtime config with the selected model injected
- `.lordcoder-model`: saved selected model
- `src/lordcoder/model_selector.py`: model selection and config rendering logic

## Troubleshooting

- If Aider is not found, restart the terminal or use `python -m uv tool run aider --config lordcoder.effective.yml`
- If an Ollama model is missing, rerun a launcher and let LordCoder pull it for you
- If your machine struggles, switch to `ollama/qwen2.5-coder:7b`

See [PERFORMANCE.md](PERFORMANCE.md) and [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for more detail.
