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

- Cross-platform dev install via `pip install .`
- Native `lordcoder.toml` config
- Stable CLI and localhost API
- Ollama runtime hardening with `/api` endpoint normalization
- Machine-readable `doctor --json` diagnostics
- Compatibility migration for `lordcoder.yml` and `.lordcoder-model`

## Quick Start

### Prerequisites

- Python 3.8+
- Ollama if you plan to use the default local runtime
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

## Runtime And Model Guidance

The current phase implements `ollama` as the only working runtime provider. `lordcoder doctor` recommends a `qwen2.5-coder` tier based on RAM and architecture, warns if the configured model is too heavy, and prints a recommended `ollama pull ...` command instead of auto-installing models.

`llama_cpp` is recognized as a planned provider, but it is not implemented in this phase.

## Project Files

- `lordcoder.toml`: native runtime/config source
- `lordcoder.yml`: legacy migration input only
- `.lordcoder-model`: legacy migration input only
- `src/lordcoder/model_selector.py`: compatibility helper for the old workflow
- `.github/workflows/`: CI and release scaffolding
- `deploy/`: service-install templates

## Roadmap

- Current phase: cross-platform dev install reliability and Ollama hardening
- Next phase: native packaging, service validation, container build validation, richer doctor checks
- Later phase: `llama.cpp`, lightweight mode, stronger distribution channels, optional LSP/OpenAPI/SDK expansion

## Troubleshooting

- Use `lordcoder doctor --json` for machine-readable diagnostics
- Use `lordcoder test --allow-shell` for policy-gated test execution
- Use `lordcoder apply --allow-write` for policy-gated file writes
- The old batch launchers remain as deprecated compatibility helpers, not the primary runtime path

See [TROUBLESHOOTING_NATIVE.md](TROUBLESHOOTING_NATIVE.md) for the native workflow and [PERFORMANCE.md](PERFORMANCE.md) for model sizing guidance.
