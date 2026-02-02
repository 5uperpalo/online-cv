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
        pdf_path: Optional path to PDF file (default: pavol_mulinka_cv.pdf in same dir as output)
    
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
        # Default: pavol_mulinka_cv.pdf in same directory as HTML
        pdf_link = "pavol_mulinka_cv.pdf"
    
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
    <a href="{pdf_link}" class="pdf-download" title="Download PDF version" download="pavol_mulinka_cv.pdf">
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


def generate_bilingual_html(cv_en_path: str, cv_es_path: str, output_path: str = "index.html",
                           pdf_en_path: Optional[str] = None, pdf_es_path: Optional[str] = None) -> str:
    """
    Generate bilingual HTML version of CV with language switcher
    
    Args:
        cv_en_path: Path to English markdown CV file
        cv_es_path: Path to Spanish markdown CV file
        output_path: Path to output HTML file
        pdf_en_path: Optional path to English PDF file
        pdf_es_path: Optional path to Spanish PDF file
    
    Returns:
        Path to generated HTML file
    """
    md_en_path = Path(cv_en_path)
    md_es_path = Path(cv_es_path)
    
    if not md_en_path.exists():
        raise FileNotFoundError(f"English markdown file not found: {cv_en_path}")
    if not md_es_path.exists():
        raise FileNotFoundError(f"Spanish markdown file not found: {cv_es_path}")
    
    # Read markdown content for both languages
    with open(md_en_path, 'r', encoding='utf-8') as f:
        md_en_content = f.read()
    
    with open(md_es_path, 'r', encoding='utf-8') as f:
        md_es_content = f.read()
    
    # Convert markdown to HTML for both languages
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
    
    html_en_content = md.convert(md_en_content)
    md.reset()
    html_es_content = md.convert(md_es_content)
    
    # Add class to Publications/Publicaciones sections for styling
    html_en_content = re.sub(
        r'<h2>Publications</h2>',
        r'<h2 class="publications-header">Publications</h2>',
        html_en_content
    )
    html_es_content = re.sub(
        r'<h2>Publicaciones</h2>',
        r'<h2 class="publications-header">Publicaciones</h2>',
        html_es_content
    )
    
    # Determine PDF paths
    output_path_obj = Path(output_path)
    pdf_en_link = pdf_en_path if pdf_en_path else "pavol_mulinka_cv.pdf"
    pdf_es_link = pdf_es_path if pdf_es_path else "pavol_mulinka_cv_es.pdf"
    
    # If PDF paths are provided, use just the filename
    if pdf_en_path:
        pdf_en_link = Path(pdf_en_path).name
    if pdf_es_path:
        pdf_es_link = Path(pdf_es_path).name
    
    # Generate bilingual HTML with language switcher
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
        /* Language switcher - Toggle style */
        .language-switcher {{
            position: fixed;
            top: 20px;
            right: 80px;
            z-index: 1001;
            display: inline-flex;
            background-color: #3498db;
            border: 2px solid #3498db;
            border-radius: 25px;
            padding: 2px;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
        }}
        .lang-btn {{
            background-color: transparent;
            color: white;
            border: none;
            padding: 8px 20px;
            border-radius: 20px;
            cursor: pointer;
            font-size: 14px;
            font-weight: 500;
            transition: all 0.3s ease;
            position: relative;
            z-index: 1;
        }}
        .lang-btn.active {{
            background-color: white;
            color: #3498db;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
        }}
        .lang-btn:not(.active):hover {{
            color: rgba(255, 255, 255, 0.8);
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
        /* Language content */
        .lang-content {{
            display: none;
        }}
        .lang-content.active {{
            display: block;
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
            .language-switcher, .pdf-download {{
                display: none;
            }}
        }}
        @media (max-width: 768px) {{
            body {{
                padding: 10px;
            }}
            .language-switcher {{
                right: 10px;
                top: 10px;
            }}
            .lang-btn {{
                padding: 6px 16px;
                font-size: 12px;
            }}
            .pdf-download {{
                top: 70px;
                right: 10px;
            }}
        }}
    </style>
</head>
<body>
    <div class="language-switcher">
        <button class="lang-btn active" onclick="switchLanguage('en')" id="btn-en">EN</button>
        <button class="lang-btn" onclick="switchLanguage('es')" id="btn-es">ES</button>
    </div>
    <a href="{pdf_en_link}" class="pdf-download" id="pdf-link" title="Download PDF version" download="pavol_mulinka_cv.pdf">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
            <path d="M14,2H6A2,2 0 0,0 4,4V20A2,2 0 0,0 6,22H18A2,2 0 0,0 20,20V8L14,2M18,20H6V4H13V9H18M12,19L8,15H11V12H13V15H16L12,19Z"/>
        </svg>
    </a>
    <div id="content-en" class="lang-content active">
        {html_en_content}
    </div>
    <div id="content-es" class="lang-content">
        {html_es_content}
    </div>
    <script>
        const pdfLinks = {{
            'en': '{pdf_en_link}',
            'es': '{pdf_es_link}'
        }};
        
        const pdfDownloads = {{
            'en': 'pavol_mulinka_cv.pdf',
            'es': 'pavol_mulinka_cv_es.pdf'
        }};
        
        function switchLanguage(lang) {{
            // Hide all content
            document.querySelectorAll('.lang-content').forEach(el => {{
                el.classList.remove('active');
            }});
            
            // Show selected language content
            document.getElementById('content-' + lang).classList.add('active');
            
            // Update button states
            document.querySelectorAll('.lang-btn').forEach(btn => {{
                btn.classList.remove('active');
            }});
            document.getElementById('btn-' + lang).classList.add('active');
            
            // Update PDF link
            const pdfLink = document.getElementById('pdf-link');
            pdfLink.href = pdfLinks[lang];
            pdfLink.download = pdfDownloads[lang];
            
            // Update HTML lang attribute
            document.documentElement.lang = lang;
            
            // Save preference to localStorage
            localStorage.setItem('preferred-language', lang);
        }}
        
        // Load saved language preference on page load
        window.addEventListener('DOMContentLoaded', function() {{
            const savedLang = localStorage.getItem('preferred-language') || 'en';
            switchLanguage(savedLang);
        }});
    </script>
</body>
</html>"""
    
    # Write HTML file
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_output)
    
    print(f"Bilingual HTML generated successfully: {output_path}")
    return str(output_path)


def setup_github_pages(output_dir: str = "docs", pdf_source: Optional[str] = None, 
                      pdf_es_source: Optional[str] = None) -> None:
    """
    Setup directory structure for GitHub Pages
    
    Args:
        output_dir: Output directory for GitHub Pages (default: docs)
        pdf_source: Optional path to source English PDF file to copy
        pdf_es_source: Optional path to source Spanish PDF file to copy
    """
    if isinstance(output_dir, str):
        docs_dir = Path(output_dir)
    else:
        docs_dir = output_dir
    
    docs_dir.mkdir(parents=True, exist_ok=True)
    
    # Create .nojekyll file to disable Jekyll processing
    nojekyll = docs_dir / ".nojekyll"
    nojekyll.touch()
    
    # Copy English PDF to docs folder for GitHub Pages
    if pdf_source:
        pdf_source_path = Path(pdf_source)
    else:
        pdf_source_path = Path("pavol_mulinka_cv.pdf")
    
    if pdf_source_path.exists():
        pdf_dest = docs_dir / pdf_source_path.name
        shutil.copy2(pdf_source_path, pdf_dest)
        print(f"English PDF copied to: {pdf_dest}")
    
    # Copy Spanish PDF to docs folder for GitHub Pages
    if pdf_es_source:
        pdf_es_source_path = Path(pdf_es_source)
    else:
        pdf_es_source_path = Path("pavol_mulinka_cv_es.pdf")
    
    if pdf_es_source_path.exists():
        pdf_es_dest = docs_dir / pdf_es_source_path.name
        shutil.copy2(pdf_es_source_path, pdf_es_dest)
        print(f"Spanish PDF copied to: {pdf_es_dest}")
    
    print(f"GitHub Pages directory setup: {docs_dir}")
