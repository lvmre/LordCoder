# LordCoder Performance Guide

This guide helps you choose the right model and keep LordCoder responsive on Windows.

## Recommended Local Models

For a system around an Intel i5-10400 with 24GB RAM:

| Model | RAM Usage | Speed | Best For |
|---|---:|---|---|
| `qwen2.5-coder:7b` | ~8GB | Fast | Quick tasks and debugging |
| `qwen2.5-coder:14b` | ~14GB | Balanced | General coding |
| `qwen2.5-coder:32b` | ~20GB | Slower | Complex tasks and larger projects |

## Switching Models

1. Launch `start-lordcoder.bat`.
2. Choose to change the saved model.
3. Pick a preset or enter a custom Aider-compatible model string.
4. If you selected an `ollama/...` model that is not installed, let LordCoder pull it.

After selection, direct launches can use:

```bash
aider --config lordcoder.effective.yml
```

## Practical Tips

- Use `qwen2.5-coder:14b` as the default local balance point.
- Drop to `qwen2.5-coder:7b` if responses are too slow or RAM is tight.
- Move up to `qwen2.5-coder:32b` only when you need better reasoning and have headroom.
- Close browsers and other heavy apps before running larger local models.
- Restart Ollama with `ollama serve` if model loading gets sluggish.

## Monitoring

You can inspect system resources with:

```bash
python src/lordcoder/utils.py
```

## Hosted Models

LordCoder also supports hosted providers through custom model strings, for example `openai/...` or `anthropic/...`. In those cases LordCoder skips Ollama checks and leaves credential validation to Aider.
