#!/usr/bin/env python3
"""
Export functions for converting CV to PDF format
"""

import subprocess
import tempfile
from pathlib import Path
from typing import Optional


def export_to_pdf(markdown_path: str, output_path: Optional[str] = None) -> str:
    """
    Export markdown CV to PDF using pandoc

    Args:
        markdown_path: Path to input markdown file
        output_path: Path to output PDF file (optional)

    Returns:
        Path to generated PDF file
    """
    md_path = Path(markdown_path)
    if not md_path.exists():
        raise FileNotFoundError(f"Markdown file not found: {markdown_path}")

    if output_path is None:
        pdf_path = md_path.with_suffix('.pdf')
    else:
        pdf_path = Path(output_path)
    
    # Check if pandoc is available
    try:
        subprocess.run(['pandoc', '--version'], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        raise RuntimeError(
            "pandoc is not installed. Please install it:\n"
            "  - macOS: brew install pandoc\n"
            "  - Linux: sudo apt-get install pandoc\n"
            "  - Windows: choco install pandoc\n"
            "Or download from: https://pandoc.org/installing.html"
        )
    
    # Create LaTeX header with enumitem for list spacing
    latex_header = r'''
\usepackage{enumitem}

% Configure enumitem to support deep nesting (up to 4 levels)
\setlistdepth{4}

% Set default list settings that work for all levels
% This ensures nested lists (including 3rd level) render correctly with proper bullets
\setlist[itemize]{leftmargin=*,itemindent=0em,label=\textbullet}
\setlist[itemize,1]{label=\textbullet}
\setlist[itemize,2]{label=\textbullet}
\setlist[itemize,3]{label=\textbullet}
\setlist[itemize,4]{label=\textbullet}

% Redefine \tightlist to be empty so enumitem settings take precedence
% This is important for Work Experience spacing and nested list rendering
\renewcommand{\tightlist}{}
'''
    
    script_dir = Path(__file__).parent
    lua_filter = script_dir / 'workexp_spacing.lua'
    
    # Create temporary file for LaTeX header
    with tempfile.NamedTemporaryFile(mode='w', suffix='.tex', delete=False) as header_file:
        header_file.write(latex_header)
        header_path = header_file.name
    
    try:
        # Convert markdown to PDF
        cmd = [
            'pandoc',
            str(md_path),
            '-o', str(pdf_path),
            '--pdf-engine=xelatex',
            '-V', 'geometry:margin=1in',
            '-V', 'colorlinks=true',
            '-V', 'linkcolor=blue',
            '-V', 'urlcolor=blue',
            '-V', 'citecolor=blue',
            '--standalone',
            '--from=markdown+raw_tex',  # Enable raw LaTeX
            '-H', header_path,  # Include LaTeX header for spacing
            '--lua-filter', str(lua_filter),  # Add spacing to Work Experience
        ]

        subprocess.run(cmd, check=True, capture_output=True)
        print(f"PDF exported successfully: {pdf_path}")
        return str(pdf_path)
    except subprocess.CalledProcessError as e:
        error_msg = e.stderr.decode() if e.stderr else "Unknown error"
        raise RuntimeError(f"Failed to generate PDF: {error_msg}")
    finally:
        # Clean up temporary header file
        try:
            Path(header_path).unlink()
        except Exception:
            pass  # Ignore cleanup errors