# LordCoder Troubleshooting Guide

This file documents the older compatibility workflow. For the current native workflow, prefer [TROUBLESHOOTING_NATIVE.md](TROUBLESHOOTING_NATIVE.md).

## Legacy Installation Issues

### `aider` command not found

Try one of these:

```bash
python -m uv tool run aider --config lordcoder.effective.yml
```

```bash
install.bat
```

### Python compatibility problems

Use the `uv` install path:

```bash
pip install uv
python -m uv tool install --force --python python3.12 aider-chat
```

## Legacy Model Selection Issues

### I want to switch models

Run:

```bash
start-lordcoder.bat
```

Then choose to change the saved model.

### My Ollama model is missing

If your selected model starts with `ollama/`, LordCoder checks whether it is installed and offers to run the matching `ollama pull ...` command.

You can also pull models manually, for example:

```bash
ollama pull qwen2.5-coder:7b
```

### I selected a hosted model

That is supported. LordCoder skips Ollama checks for non-`ollama/...` models. Any provider credential errors will come from Aider itself.

## Legacy Performance Issues

### Responses are too slow

- Switch to `ollama/qwen2.5-coder:7b`
- Close unnecessary applications
- Restart Ollama with `ollama serve`

### Out of memory

- Switch to a smaller model
- Close browsers and other heavy applications
- Reboot if Ollama has accumulated memory pressure

## Legacy Debugging

Check the generated runtime config:

```bash
aider --config lordcoder.effective.yml --version
```

Verbose launch:

```bash
aider --config lordcoder.effective.yml --verbose
```

Inspect local system resources:

```bash
python src/lordcoder/utils.py
```
