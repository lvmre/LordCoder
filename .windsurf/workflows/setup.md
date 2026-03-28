---
description: Initialize LordCoder development environment
---

# LordCoder Setup Workflow

This workflow sets up the complete LordCoder AI development environment.

## Steps

1. **Create virtual environment**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```

2. **Install dependencies**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

3. **Install Ollama model**
   ```bash
   ollama pull qwen2.5-coder:32b
   ```

4. **Start LordCoder**
   ```bash
   aider --config lordcoder.yml
   ```

## Usage

Run this workflow when setting up LordCoder on a new machine or after cloning the repository.

## Troubleshooting

- If Ollama is not installed, download from https://ollama.com
- For systems with less RAM, use: `ollama pull qwen2.5-coder:7b`
- Update lordcoder.yml to use the smaller model if needed
