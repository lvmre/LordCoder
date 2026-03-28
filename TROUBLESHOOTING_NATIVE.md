# LordCoder Native Troubleshooting Guide

## Install Issues

### `lordcoder` command not found

Try:

```bash
python -m lordcoder --version
```

If that works, your Python scripts directory is not on `PATH`.

### `pip install .` fails

If a local `pip install .` fails:

- ensure `%TEMP%` / `%TMP%` point to writable directories on Windows
- try inside a virtual environment
- rerun `python -m pip install .`

## Runtime Issues

### Ollama is not reachable

Run:

```bash
lordcoder doctor
```

Check the runtime section for:

- configured endpoint
- executable presence
- installed model list
- recommended model command

The native Ollama endpoint should be:

```text
http://127.0.0.1:11434/api
```

### Configured model is not installed

LordCoder does not auto-pull models in this phase. Use the command shown by `lordcoder doctor`, for example:

```bash
ollama pull qwen2.5-coder:7b
```

### Configured model is too heavy

`lordcoder doctor` warns when the configured model is larger than the recommended tier for the machine. Update `lordcoder.toml` to a smaller model if needed.

### `llama_cpp` is configured

`llama_cpp` is a planned provider in this phase, not an implemented runtime. LordCoder reports that clearly instead of pretending it works.

## Command Issues

### File writes are blocked

Re-run the command with:

```bash
lordcoder apply --allow-write ...
```

### Test execution is blocked

Re-run the command with:

```bash
lordcoder test --allow-shell
```

## Debugging

Get machine-readable diagnostics:

```bash
lordcoder doctor --json
```

Check daemon health:

```bash
curl http://127.0.0.1:32123/healthz
```

Legacy batch launchers and the older model selector still exist for compatibility, but they are not the primary runtime path anymore.
