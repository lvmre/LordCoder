# LordCoder Performance Guide

This guide covers the current native LordCoder workflow and its model-sizing guidance.

## Recommended Local Models

LordCoder currently recommends `qwen2.5-coder` tiers based on RAM and architecture:

| Machine Class | Recommended Model | Notes |
|---|---|---|
| Low RAM or `armv7` | `qwen2.5-coder:1.5b` | Safest starting point |
| Under 16 GB RAM | `qwen2.5-coder:7b` | Good for quick edits and debugging |
| 16-32 GB RAM | `qwen2.5-coder:14b` | Balanced default for general coding |
| 32+ GB RAM | `qwen2.5-coder:32b` | Larger-context, slower local work |

## How To Check The Recommendation

Run:

```bash
lordcoder doctor
```

Or machine-readable output:

```bash
lordcoder doctor --json
```

LordCoder will:

- recommend a model tier
- warn when the configured model is too heavy
- show whether the configured Ollama model is installed
- print a recommended `ollama pull ...` command when it is missing

## Practical Tips

- Use `qwen2.5-coder:14b` as the balanced default on a typical 16-32 GB dev machine.
- Drop to `qwen2.5-coder:7b` or `qwen2.5-coder:1.5b` if responses are too slow or RAM is tight.
- Move up to `qwen2.5-coder:32b` only when you have clear headroom.
- Close browsers and other heavy apps before loading larger local models.
- Restart Ollama if model loading gets sluggish.

## Monitoring

Inspect system resources:

```bash
python src/lordcoder/utils.py
```

Inspect native diagnostics:

```bash
lordcoder doctor --json
```

## Planned Runtime Expansion

`llama_cpp` is part of the roadmap for lower-RAM and ARM-focused setups, but it is not implemented in the current phase. For now, Ollama is the only supported runtime.
