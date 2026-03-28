---
description: Git commit automation for LordCoder
---

# LordCoder Commit Workflow

This workflow handles git commits with proper formatting and validation.

## Steps

1. **Check git status**

   ```bash
   git status
   ```

2. **Add all changes**

   ```bash
   git add .
   ```

3. **Create commit with descriptive message**

   ```bash
   git commit -m "feat: add system monitoring utilities with comprehensive tests

   - Add SystemMonitor class with disk/memory/CPU monitoring
   - Implement error handling and fallbacks
   - Add comprehensive test suite with 95%+ coverage
   - Create package structure with proper type hints
   - Add Windows setup scripts and documentation"
   ```

4. **Push to remote (if needed)**

   ```bash
   git push origin main
   ```

## Commit Message Format

Use conventional commits:
- `feat:` for new features
- `fix:` for bug fixes
- `docs:` for documentation changes
- `test:` for test-related changes
- `refactor:` for code refactoring

## Usage

Run this workflow after completing development work to commit changes properly.
