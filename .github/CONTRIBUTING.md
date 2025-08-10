# Contributing to Crashlens Detector

Thank you for your interest in contributing to Crashlens Detector! This document outlines the process for contributing to this project.

## 🚀 Quick Start

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/crashlens-detector.git
   cd crashlens-detector
   ```
3. **Set up the development environment**:
   ```bash
   # Install Poetry (if not already installed)
   curl -sSL https://install.python-poetry.org | python3 -

   # Install dependencies
   poetry install

   # Activate virtual environment
   poetry shell
   ```

## 🔄 Development Workflow

### Creating a Feature Branch

Always create a new branch for your work:

```bash
# Create and switch to a new branch
git checkout -b feature/your-feature-name

# Or for bug fixes
git checkout -b fix/issue-description
```

**Never commit directly to the `main` branch!**

### Making Changes

1. **Write clean, focused commits**:
   ```bash
   git add .
   git commit -m "feat: add new detector for model switching patterns"
   ```

2. **Follow conventional commits** (recommended):
   - `feat:` for new features
   - `fix:` for bug fixes  
   - `docs:` for documentation changes
   - `test:` for test additions/changes
   - `refactor:` for code refactoring
   - `chore:` for maintenance tasks

3. **Test your changes**:
   ```bash
   # Run tests
   pytest

   # Run linting
   poetry run black crashlens/
   poetry run flake8 crashlens/

   # Test the CLI
   poetry run crashlens scan examples-logs/demo-logs.jsonl
   ```

### Submitting a Pull Request

1. **Push your branch**:
   ```bash
   git push origin feature/your-feature-name
   ```

2. **Open a Pull Request** on GitHub with:
   - Clear title describing the change
   - Detailed description of what you've implemented
   - Reference any related issues (`Fixes #123`)
   - Include examples or screenshots if applicable

3. **PR Requirements** (enforced by branch protection):
   - ✅ At least **1 approval** required before merging
   - ✅ All **conversations must be resolved**
   - ✅ **Status checks must pass** (tests, linting, etc.)
   - ✅ Branch must be **up-to-date** with main before merging

## 🧪 Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=crashlens

# Run specific test file
pytest tests/test_rules.py -v
```

### Adding Tests

- Add tests for new detectors in `tests/`
- Test files should be named `test_*.py`
- Use descriptive test names: `test_retry_loop_detector_flags_excessive_retries`

## 🎨 Code Style

We use automated formatting and linting:

```bash
# Format code
poetry run black crashlens/ tests/

# Check linting
poetry run flake8 crashlens/ tests/

# Type checking (optional but recommended)
poetry run mypy crashlens/
```

### Code Style Guidelines

- **Python 3.12+** required
- Follow **PEP 8** style guide
- Use **type hints** where possible
- Write **docstrings** for public functions
- Keep functions **focused and small**

## 🔐 Commit Signing (Recommended)

For enhanced security, consider signing your commits:

1. **Set up GPG key**:
   ```bash
   # Generate GPG key (if you don't have one)
   gpg --gen-key

   # List your keys
   gpg --list-secret-keys --keyid-format LONG

   # Add key to GitHub account (copy the public key)
   gpg --armor --export YOUR_KEY_ID
   ```

2. **Configure Git**:
   ```bash
   git config --global commit.gpgsign true
   git config --global user.signingkey YOUR_KEY_ID
   ```

## 📝 Documentation

- Update `README.md` if adding new features
- Add docstrings to new detectors and functions
- Update `detectors.md` if modifying detection logic
- Include examples in your documentation

## 🐛 Reporting Issues

When reporting bugs:

1. **Check existing issues** first
2. **Use the issue template** (if available)
3. **Include**:
   - Python version
   - Operating system
   - Steps to reproduce
   - Expected vs actual behavior
   - Sample log files (anonymized)

## 🎯 Types of Contributions

We welcome:

- 🔍 **New detectors** for different waste patterns
- 🐛 **Bug fixes** and improvements
- 📚 **Documentation** enhancements  
- 🧪 **Test coverage** improvements
- 🎨 **Code quality** improvements
- 💡 **Performance optimizations**

## 📋 Checklist for Contributors

Before submitting your PR:

- [ ] Code follows the style guidelines
- [ ] Tests pass locally (`pytest`)
- [ ] New functionality includes tests
- [ ] Documentation is updated
- [ ] Commit messages are clear
- [ ] Branch is up-to-date with main
- [ ] No merge conflicts

## 🤝 Code of Conduct

- Be respectful and inclusive
- Focus on constructive feedback
- Help newcomers get started
- Keep discussions on-topic

## 💬 Getting Help

- 💬 **Discussions**: Use GitHub Discussions for questions
- 🐛 **Issues**: Report bugs via GitHub Issues
- 📧 **Email**: For private matters, contact the maintainers

## 🏆 Recognition

Contributors will be:
- Listed in the project README
- Mentioned in release notes
- Invited to become maintainers (for regular contributors)

---

Thank you for contributing to Crashlens Detector! Your help makes this tool better for the entire AI development community. 🎉
