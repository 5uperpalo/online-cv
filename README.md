# The Most LLM-Friendly CV Ever

A simple CV management tool that supports three core operations:
1. **Regenerate Publications** - Update the Publications section from `bibliography.bib`
2. **Export** - Export CV to PDF format
3. **Publish to Web** - Generate HTML version for web publishing

## Quick Start

### Installation

```bash
# Create virtual environment
python -m venv the-most-llm-friendly-cv-ever
source the-most-llm-friendly-cv-ever/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install pandoc (for PDF export)
# macOS: brew install pandoc
# Linux: sudo apt-get install pandoc
# Windows: choco install pandoc
```

## Usage

### 1. Regenerate Publications Section

Update the Publications section in your CV from `bibliography.bib`:

```bash
python main.py --regenerate-publications
```

This will:
- Parse `bibliography.bib`
- Extract all publications
- Sort them by date (newest first)
- Replace the Publications section in `cv.md`

### 2. Export CV

Export your CV to PDF:

```bash
# Export to PDF
python main.py --export-pdf
```

### 3. Publish to Web

Generate HTML version for web publishing:

```bash
python main.py --publish-web
```

This will:
- Generate `docs/index.html` from your CV
- Setup GitHub Pages directory structure
- Create `.nojekyll` file for GitHub Pages

You can specify a custom output path:

```bash
python main.py --publish-web --web-output path/to/index.html
```

## Options

```bash
python main.py [OPTIONS]

Options:
  --regenerate-publications    Regenerate Publications section from bibliography.bib
  --export-pdf                 Export CV to PDF format
  --publish-web                 Generate HTML version for web publishing
  --web-output PATH             Output HTML file path (default: docs/index.html)
  --cv-file PATH                Path to CV markdown file (default: cv.md)
```

## GitHub Pages Deployment

After running `--publish-web`, you can deploy to GitHub Pages:

1. Push the `docs/` directory to your repository
2. Enable GitHub Pages in repository settings
3. Point it to the `docs` folder

Your CV will be available at: `https://<username>.github.io/<repo-name>/`

## Examples

```bash
# Regenerate publications and export to PDF
python main.py --regenerate-publications --export-pdf

# Generate web version
python main.py --publish-web

# All operations at once
python main.py --regenerate-publications --export-pdf --publish-web
```

## Troubleshooting

### Pandoc Not Found
Make sure pandoc is installed and in your PATH:
```bash
pandoc --version
```

### Publications Section Not Found
Make sure your `cv.md` has a `## Publications` section.

### Bibliography Parse Errors
Check that `bibliography.bib` is valid BibTeX format.
