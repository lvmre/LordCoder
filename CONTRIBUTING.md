# Contributing to LordCoder

Thank you for your interest in contributing to LordCoder! This document provides guidelines for contributors.

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- Git
- 24GB RAM (for qwen2.5-coder:32b model)
- Windows 10/11 (primary target, but contributions for other platforms welcome)

### Setup

1. **Fork the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/LordCoder.git
   cd LordCoder
   ```

2. **Set up development environment**
   ```bash
   # Run the setup script
   install.bat
   
   # Or set up manually
   python -m venv .venv
   .venv\Scripts\activate
   pip install -r requirements.txt
   pip install -e .[dev]
   ```

3. **Install development dependencies**
   ```bash
   pip install black flake8 mypy pytest-cov
   ```

## 🛠️ Development Workflow

### 1. Create a Feature Branch

```bash
git checkout -b feature/your-feature-name
```

### 2. Make Your Changes

- Follow the existing code style
- Add type hints to all new functions
- Write comprehensive tests
- Update documentation as needed

### 3. Run Tests

```bash
# Run all tests
pytest tests/ --cov=src/lordcoder

# Run specific tests
pytest tests/test_utils.py -v

# Check code style
black --check src/ tests/
flake8 src/ tests/
mypy src/
```

### 4. Commit Your Changes

Use conventional commit messages:

```bash
git commit -m "feat: add new system monitoring feature

- Add CPU temperature monitoring
- Update documentation
- Add comprehensive tests"
```

### 5. Push and Create Pull Request

```bash
git push origin feature/your-feature-name
```

Then create a pull request on GitHub.

## 📝 Code Style Guidelines

### Python Code

- Use **Black** for code formatting
- Use **type hints** for all functions
- Write **docstrings** for all public functions and classes
- Follow **PEP 8** style guidelines
- Use **f-strings** for string formatting

### Example

```python
def calculate_disk_usage(path: str) -> DiskUsage:
    """
    Calculate disk usage for the given path.
    
    Args:
        path: The path to analyze
        
    Returns:
        DiskUsage object with usage information
        
    Raises:
        OSError: If the path doesn't exist
    """
    if not os.path.exists(path):
        raise OSError(f"Path does not exist: {path}")
    
    # Implementation here
    return disk_usage
```

### Testing

- Write **unit tests** for all new functions
- Use **descriptive test names**
- Test **error conditions** and edge cases
- Aim for **90%+ test coverage**

### Example Test

```python
def test_calculate_disk_usage_valid_path(self) -> None:
    """Test calculating disk usage for a valid path."""
    result = calculate_disk_usage(".")
    self.assertIsInstance(result, DiskUsage)
    self.assertGreater(result.total, 0)
```

## 🐛 Bug Reports

When reporting bugs, please include:

1. **Python version**
2. **Operating system**
3. **LordCoder version**
4. **Steps to reproduce**
5. **Expected vs actual behavior**
6. **Error messages and logs**

Use the issue template on GitHub.

## 💡 Feature Requests

Feature requests are welcome! Please:

1. **Check existing issues** first
2. **Describe the use case** clearly
3. **Explain why it's valuable**
4. **Suggest implementation** if possible

## 📚 Documentation

- Update **README.md** for user-facing changes
- Update **CONTRIBUTING.md** for development changes
- Add **docstrings** for all new APIs
- Include **examples** in documentation

## 🔧 Development Tools

### Code Formatting

```bash
# Format code
black src/ tests/

# Check formatting
black --check src/ tests/
```

### Linting

```bash
# Run flake8
flake8 src/ tests/

# Run mypy
mypy src/
```

### Testing

```bash
# Run tests with coverage
pytest tests/ --cov=src/lordcoder --cov-report=html

# Run tests with verbose output
pytest tests/ -v
```

## 🏆 Types of Contributions

We welcome various types of contributions:

### 🐛 Bug Fixes
- Fix issues in existing code
- Improve error handling
- Fix failing tests

### ✨ New Features
- Add new system monitoring capabilities
- Improve the LordCoder AI personality
- Add new utility functions

### 📚 Documentation
- Improve README and guides
- Add examples and tutorials
- Fix typos and clarify explanations

### 🧪 Testing
- Improve test coverage
- Add integration tests
- Fix flaky tests

### 🛠️ Infrastructure
- Improve CI/CD pipelines
- Update dependencies
- Improve build scripts

## 🤝 Code Review Process

1. **Automated checks** must pass
2. **At least one maintainer** review required
3. **All discussions** resolved
4. **Tests updated** if needed
5. **Documentation updated** if needed

## 📋 Pull Request Checklist

Before submitting a PR, ensure:

- [ ] Code follows style guidelines
- [ ] All tests pass
- [ ] Test coverage is maintained
- [ ] Documentation is updated
- [ ] Commit messages are conventional
- [ ] PR description is clear
- [ ] No merge conflicts

## 🎯 Release Process

Maintainers will:

1. **Review and merge** PRs
2. **Update version** in setup.py
3. **Create release tag**
4. **Update CHANGELOG**
5. **Publish to PyPI** (if applicable)

## 💬 Getting Help

- **GitHub Issues**: For bugs and feature requests
- **Discussions**: For general questions
- **Email**: github@lvmre.dev for private matters

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

## 🙏 Recognition

Contributors are recognized in:
- README.md contributors section
- Release notes
- Commit history

Thank you for contributing to LordCoder! 🚀
