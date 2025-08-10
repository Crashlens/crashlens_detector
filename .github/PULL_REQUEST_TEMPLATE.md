## Pull Request Checklist

Please ensure your PR meets the following requirements before submitting:

### 📋 Pre-submission Checklist

- [ ] **Branch**: Created from `main` and targeting `main`
- [ ] **Tests**: All tests pass locally (`poetry run pytest`)
- [ ] **Linting**: Code follows style guidelines (`poetry run black . && poetry run flake8`)
- [ ] **Type Checking**: No type errors (`poetry run mypy crashlens/`)
- [ ] **CLI Testing**: Tool works as expected (`poetry run crashlens --version`)

### 📝 Description

**What does this PR do?**
<!-- Provide a clear and concise description of the changes -->

**Why is this change needed?**
<!-- Explain the motivation or issue this addresses -->

**Related Issues:**
<!-- Link any related issues: Fixes #123, Closes #456 -->

### 🧪 Testing

**How was this tested?**
<!-- Describe the tests you ran and their results -->

**Test Coverage:**
- [ ] Added tests for new functionality
- [ ] Updated existing tests if needed
- [ ] All tests pass

### 📚 Documentation

- [ ] Updated relevant documentation
- [ ] Added docstrings to new functions
- [ ] Updated `detectors.md` if detection logic changed

### 🔄 Type of Change

- [ ] 🐛 Bug fix (non-breaking change that fixes an issue)
- [ ] ✨ New feature (non-breaking change that adds functionality)  
- [ ] 💥 Breaking change (fix or feature that would cause existing functionality to change)
- [ ] 📚 Documentation update
- [ ] 🧪 Test improvements
- [ ] 🎨 Code style/formatting changes

### 🚀 Additional Notes

<!-- Any additional information, context, or screenshots -->

### 📸 Screenshots (if applicable)

<!-- Include screenshots for UI changes or CLI output -->

---

**By submitting this PR, I confirm that:**

- [ ] I have read and followed the [Contributing Guidelines](CONTRIBUTING.md)
- [ ] My code follows the project's style guidelines
- [ ] I have performed a self-review of my code
- [ ] I have commented my code, particularly in hard-to-understand areas
- [ ] My changes generate no new warnings
- [ ] I have added tests that prove my fix is effective or that my feature works
- [ ] New and existing unit tests pass locally with my changes
