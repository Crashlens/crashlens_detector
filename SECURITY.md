# Security Policy

## Supported Versions

We actively maintain and provide security updates for the following versions:

| Version | Supported          |
| ------- | ------------------ |
| 1.2.x   | ✅ Yes            |
| 1.1.x   | ✅ Yes            |
| 1.0.x   | ⚠️ Limited support |
| < 1.0   | ❌ No             |

## Reporting a Vulnerability

We take security seriously at Crashlens Detector. If you discover a security vulnerability, please follow these steps:

### 🔒 Private Reporting (Preferred)

1. **Do NOT create a public GitHub issue** for security vulnerabilities
2. **Email us directly** at: `security@crashlens.dev` (or use GitHub's private vulnerability reporting)
3. **Include the following information**:
   - Description of the vulnerability
   - Steps to reproduce the issue
   - Potential impact assessment
   - Suggested fix (if you have one)

### 📧 What to Include

- **Crashlens Detector version** affected
- **Operating system** and Python version
- **Detailed description** of the vulnerability
- **Proof of concept** code or steps to reproduce
- **Your contact information** for follow-up

### ⏰ Response Timeline

- **Initial response**: Within 48 hours
- **Triage and assessment**: Within 7 days  
- **Fix development**: 2-4 weeks (depending on severity)
- **Public disclosure**: After fix is released

### 🏆 Recognition

We appreciate security researchers who help keep our users safe:

- **Acknowledgment** in our security advisories (if desired)
- **Credit** in release notes
- **Priority support** for future questions

## Security Considerations

### 🔐 Data Privacy

Crashlens Detector processes log files locally and does not send data to external services. However, be aware that:

- **Log files may contain sensitive information** (prompts, responses, API keys)
- **Use PII scrubbing features** when sharing logs or reports
- **Review generated reports** before sharing publicly

### 🛡️ Safe Usage

- **Keep Crashlens Detector updated** to the latest version
- **Validate log files** from untrusted sources
- **Use virtual environments** for isolation
- **Review permissions** when running in automated environments

### 📋 Known Security Considerations

1. **Log File Processing**: Crashlens processes JSONL files which could theoretically contain malicious content
2. **File System Access**: The tool reads/writes files in the specified directories
3. **Dependencies**: Security depends on the security of our Python dependencies

## Vulnerability Categories

We're particularly interested in reports about:

- **Code injection** through log file processing
- **Path traversal** vulnerabilities  
- **Denial of service** through malformed inputs
- **Information disclosure** beyond intended functionality
- **Dependency vulnerabilities** in our supply chain

## Out of Scope

The following are generally **not** considered security vulnerabilities:

- Issues requiring physical access to the machine
- Social engineering attacks
- Vulnerabilities in dependencies that don't affect our usage
- Issues in unsupported versions
- Performance issues that don't constitute DoS

## Contact Information

- **Security Email**: `security@crashlens.dev`
- **General Issues**: [GitHub Issues](https://github.com/Crashlens/crashlens-detector/issues)
- **Maintainer**: @Crashlens

---

Thank you for helping keep Crashlens Detector and our community safe! 🛡️
