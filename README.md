# LordCoder

LordCoder is a local AI coding assistant built around Aider. It gives you reusable Windows launchers, a checked-in base config, and a persisted model selector so you can switch between local and hosted LLMs without editing the repo config by hand.

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
install.bat
```

Manual with `uv`:

```bash
pip install uv
python -m uv tool install --force --python python3.12 aider-chat
```

Traditional virtual environment:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install --upgrade pip
pip install aider-chat==0.13.0 psutil pytest pytest-cov
```

If you want local Ollama models, install Ollama from <https://ollama.com>. LordCoder will offer to pull the selected Ollama model when you launch it.

### Launch

Recommended launcher:

```bash
start-lordcoder.bat
```

Alternate launcher:

```bash
run-lordcoder.bat
```

After a model has been selected once, you can also launch Aider directly with the generated runtime config:

```bash
aider --config lordcoder.effective.yml
```

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
