---
description: Run LordCoder test suite
---

# LordCoder Test Workflow

This workflow runs the complete test suite for LordCoder utilities.

## Steps

1. **Activate virtual environment**

   ```bash
   .venv\Scripts\activate
   ```

2. **Run tests with coverage**

   ```bash
   pytest tests/ --cov=src/lordcoder --cov-report=html --cov-report=term
   ```

3. **Run specific test file**

   ```bash
   pytest tests/test_utils.py -v
   ```

4. **Run tests with verbose output**

   ```bash
   pytest tests/ -v --tb=short
   ```

## Usage

Run this workflow after making changes to verify everything works correctly.

## Test Coverage

The test suite covers:
- SystemMonitor class functionality
- Disk usage calculations
- Memory information retrieval
- Error handling scenarios
- Integration tests
