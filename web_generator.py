#!/usr/bin/env python3
"""
Web generator for creating GitHub Pages compatible HTML version
"""

from pathlib import Path
from datetime import datetime
from typing import Optional
import re
import shutil
import markdown
from markdown.extensions import codehilite, fenced_code, tables
# Import to register the extension with markdown
import mdx_truly_sane_lists  # noqa: F401


def generate_html(cv_markdown_path: str, output_path: str = "index.html", 
                  template_path: Optional[str] = None, pdf_path: Optional[str] = None) -> str:
    """
    Generate HTML version of CV for GitHub Pages
    
    Args:
        cv_markdown_path: Path to markdown CV file
        output_path: Path to output HTML file
        template_path: Optional custom HTML template
        pdf_path: Optional path to PDF file (default: cv.pdf in same dir as output)
    
    Returns:
        Path to generated HTML file
    """
    md_path = Path(cv_markdown_path)
    if not md_path.exists():
        raise FileNotFoundError(f"Markdown file not found: {cv_markdown_path}")
    
    # Read markdown content
    with open(md_path, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    # Convert markdown to HTML
    md = markdown.Markdown(extensions=[
        'codehilite',
        'fenced_code',
        'tables',
        'nl2br',
        'mdx_truly_sane_lists',
        ],
        extension_configs={
            "mdx_truly_sane_lists": {
                "nested_indent": 2,
                "truly_sane": True,
            }
        }
    )
    html_content = md.convert(md_content)
    
    # Add class to Publications section for styling
    html_content = re.sub(
        r'<h2>Publications</h2>',
        r'<h2 class="publications-header">Publications</h2>',
        html_content
    )
    
    # Determine PDF path for download link
    # PDF will be copied to same directory as HTML output, so use same directory
    output_path_obj = Path(output_path)
    if pdf_path:
        pdf_path_obj = Path(pdf_path)
        # Use just the filename since PDF will be copied to same dir as HTML
        pdf_link = pdf_path_obj.name
    else:
        # Default: cv.pdf in same directory as HTML
        pdf_link = "cv.pdf"
    
    # Create HTML template
    if template_path and Path(template_path).exists():
        with open(template_path, 'r', encoding='utf-8') as f:
            html_template = f.read()
        html_output = html_template.replace('{{CONTENT}}', html_content)
    else:
        # Default template
        html_output = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CV - The Most LLM-Friendly CV Ever</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            line-height: 1.6;
            max-width: 900px;
            margin: 0 auto;
            padding: 20px;
            color: #333;
            background-color: #fff;
        }}
        h1 {{
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
        }}
        h2 {{
            color: #34495e;
            margin-top: 30px;
            border-bottom: 2px solid #ecf0f1;
            padding-bottom: 5px;
        }}
        h3 {{
            color: #7f8c8d;
        }}
        code {{
            background-color: #f4f4f4;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: 'Courier New', monospace;
        }}
        pre {{
            background-color: #f4f4f4;
            padding: 15px;
            border-radius: 5px;
            overflow-x: auto;
        }}
        a {{
            color: #3498db;
            text-decoration: none;
        }}
        a:hover {{
            text-decoration: underline;
        }}
        ul, ol {{
            margin: 10px 0;
            padding-left: 30px;
        }}
        li {{
            margin: 5px 0;
        }}
        table {{
            border-collapse: collapse;
            width: 100%;
            margin: 20px 0;
        }}
        th, td {{
            border: 1px solid #ddd;
            padding: 12px;
            text-align: left;
        }}
        th {{
            background-color: #3498db;
            color: white;
        }}
        tr:nth-child(even) {{
            background-color: #f2f2f2;
        }}
        /* Publications section - smaller font for list items */
        .publications-header + ul li {{
            font-size: 0.9em;
            line-height: 1.5;
        }}
        /* PDF Download icon */
        .pdf-download {{
            position: fixed;
            top: 20px;
            right: 20px;
            z-index: 1000;
            background-color: #3498db;
            color: white;
            width: 48px;
            height: 48px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
            transition: all 0.3s ease;
            text-decoration: none;
        }}
        .pdf-download:hover {{
            background-color: #2980b9;
            transform: scale(1.1);
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
        }}
        .pdf-download svg {{
            width: 24px;
            height: 24px;
            fill: white;
        }}
        .footer {{
            margin-top: 50px;
            padding-top: 20px;
            border-top: 1px solid #ecf0f1;
            text-align: center;
            color: #7f8c8d;
            font-size: 0.9em;
        }}
        @media print {{
            body {{
                max-width: 100%;
                padding: 0;
            }}
        }}
        @media (max-width: 768px) {{
            body {{
                padding: 10px;
            }}
        }}
    </style>
</head>
<body>
    <a href="{pdf_link}" class="pdf-download" title="Download PDF version" download="cv.pdf">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
            <path d="M14,2H6A2,2 0 0,0 4,4V20A2,2 0 0,0 6,22H18A2,2 0 0,0 20,20V8L14,2M18,20H6V4H13V9H18M12,19L8,15H11V12H13V15H16L12,19Z"/>
        </svg>
    </a>
    {html_content}
</body>
</html>"""
    
    # Write HTML file
    output_path = Path(output_path)
    # Create parent directory if it doesn't exist
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_output)
    
    print(f"HTML generated successfully: {output_path}")
    return str(output_path)


def setup_github_pages(output_dir: str = "docs", pdf_source: Optional[str] = None) -> None:
    """
    Setup directory structure for GitHub Pages
    
    Args:
        output_dir: Output directory for GitHub Pages (default: docs)
        pdf_source: Optional path to source PDF file to copy (default: cv.pdf)
    """
    if isinstance(output_dir, str):
        docs_dir = Path(output_dir)
    else:
        docs_dir = output_dir
    
    docs_dir.mkdir(parents=True, exist_ok=True)
    
    # Create .nojekyll file to disable Jekyll processing
    nojekyll = docs_dir / ".nojekyll"
    nojekyll.touch()
    
    # Copy PDF to docs folder for GitHub Pages
    if pdf_source:
        pdf_source_path = Path(pdf_source)
    else:
        pdf_source_path = Path("cv.pdf")
    
    if pdf_source_path.exists():
        pdf_dest = docs_dir / pdf_source_path.name
        shutil.copy2(pdf_source_path, pdf_dest)
        print(f"PDF copied to: {pdf_dest}")
    
    print(f"GitHub Pages directory setup: {docs_dir}")
