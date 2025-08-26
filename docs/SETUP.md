# Tailored Apply Bot - Setup Guide

## Prerequisites

- Python 3.7 or higher
- Git (for version control)
- Text editor or IDE of your choice

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/Tanarius/tailored-apply-bot.git
cd tailored-apply-bot
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Verify Installation
```bash
python tailored-apply-interactive.py --help
```

## Configuration

### Resume Templates
The bot uses template-based resume generation. Ensure your base resume templates are properly formatted and accessible to the application.

### Job Data Input
The system accepts job postings in multiple formats:
- Text files containing job descriptions
- Direct text input through interactive mode
- Structured job data in JSON format

## Basic Usage

### Interactive Mode (Recommended for first use)
```bash
python tailored-apply-interactive.py
```

### Automated Processing
```bash
python tailored-apply-bot.py
```

### Job Search Integration
```bash
python job-bot.py
```

## Troubleshooting

### Common Issues

**Issue**: Module not found errors
**Solution**: Ensure all dependencies are installed with `pip install -r requirements.txt`

**Issue**: File path errors
**Solution**: Verify that resume templates and job data files are in the correct locations

**Issue**: Formatting problems in generated documents
**Solution**: Check that input templates are properly formatted and contain required placeholders

## System Requirements

- **Memory**: Minimum 512MB RAM
- **Storage**: 100MB free space for application and temporary files
- **Network**: Internet connection for any API-based enhancements (optional)

## Support

For issues, questions, or contributions:
- Create an issue on the GitHub repository
- Review the DEVELOPMENT_LOG.md for implementation details
- Check examples/ directory for usage patterns

---

Built as part of Infrastructure → AI/Automation career transition by Trey Ellingson