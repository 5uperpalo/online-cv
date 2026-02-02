#!/usr/bin/env python3
"""
Main entry point for CV operations
Supports:
1. Regenerate Publications section from bibliography.bib
2. Export CV to PDF
3. Publish CV to web (HTML)
"""

import argparse
import sys
from pathlib import Path
from cv_generator import CVGenerator
from exporters import export_to_pdf
from web_generator import generate_html, generate_bilingual_html, setup_github_pages


def main():
    parser = argparse.ArgumentParser(
        description='CV Management Tool - Regenerate publications, export, or publish to web'
    )

    # Option 1: Regenerate publications
    parser.add_argument(
        '--regenerate-publications',
        action='store_true',
        help='Regenerate Publications section from bibliography.bib'
    )

    # Option 2: Export to PDF
    parser.add_argument(
        '--export-pdf',
        action='store_true',
        help='Export CV to PDF format'
    )

    # Option 3: Publish to web
    parser.add_argument(
        '--publish-web',
        action='store_true',
        help='Generate HTML version and setup for web publishing'
    )
    parser.add_argument(
        '--web-output',
        default='docs/index.html',
        help='Output HTML file path for web version (default: docs/index.html)'
    )

    # Optional: specify CV file
    parser.add_argument(
        '--cv-file',
        default='pavol_mulinka_cv.md',
        help='Path to CV markdown file (default: pavol_mulinka_cv.md)'
    )
    parser.add_argument(
        '--cv-file-es',
        default='pavol_mulinka_cv_es.md',
        help='Path to Spanish CV markdown file (default: pavol_mulinka_cv_es.md)'
    )
    parser.add_argument(
        '--bilingual',
        action='store_true',
        help='Generate bilingual HTML with language switcher (requires both --cv-file and --cv-file-es)'
    )

    args = parser.parse_args()

    # If no action specified, show help
    if not any([args.regenerate_publications, args.export_pdf, args.publish_web]):
        parser.print_help()
        return

    cv_path = Path(args.cv_file)

    # Option 1: Regenerate publications
    if args.regenerate_publications:
        print("Regenerating Publications section from bibliography.bib...")
        try:
            generator = CVGenerator(cv_path=str(cv_path))
            updated_path = generator.regenerate_publications()
            print(f"✓ Publications section updated in: {updated_path}")
        except Exception as e:
            print(f"✗ Error: {e}", file=sys.stderr)
            sys.exit(1)

    # Option 2: Export to PDF
    if args.export_pdf:
        print(f"Exporting {cv_path} to PDF...")
        try:
            pdf_path = export_to_pdf(str(cv_path))
            print(f"✓ PDF exported: {pdf_path}")
        except Exception as e:
            print(f"✗ Error: {e}", file=sys.stderr)
            sys.exit(1)

    # Option 3: Publish to web
    if args.publish_web:
        try:
            cv_es_path = Path(args.cv_file_es)
            
            # Check if bilingual mode is requested
            if args.bilingual:
                print(f"Generating bilingual web version from {cv_path} and {cv_es_path}...")
                if not cv_es_path.exists():
                    print(f"Warning: Spanish CV file not found: {cv_es_path}", file=sys.stderr)
                    print("Falling back to English-only version...")
                    args.bilingual = False
            
            if args.bilingual:
                # Generate bilingual HTML
                # Look for PDF files
                pdf_en_file = Path("pavol_mulinka_cv.pdf")
                pdf_es_file = Path("pavol_mulinka_cv_es.pdf")
                pdf_en_path = str(pdf_en_file) if pdf_en_file.exists() else None
                pdf_es_path = str(pdf_es_file) if pdf_es_file.exists() else None
                
                html_path = generate_bilingual_html(
                    str(cv_path), 
                    str(cv_es_path), 
                    args.web_output,
                    pdf_en_path=pdf_en_path,
                    pdf_es_path=pdf_es_path
                )
                setup_github_pages(
                    Path(args.web_output).parent, 
                    pdf_source=pdf_en_path,
                    pdf_es_source=pdf_es_path
                )
                print(f"✓ Bilingual web version generated: {html_path}")
            else:
                # Generate single-language HTML
                print(f"Generating web version from {cv_path}...")
                pdf_file = Path("pavol_mulinka_cv.pdf")
                pdf_path = str(pdf_file) if pdf_file.exists() else None
                html_path = generate_html(str(cv_path), args.web_output, pdf_path=pdf_path)
                setup_github_pages(Path(args.web_output).parent, pdf_source=pdf_path)
                print(f"✓ Web version generated: {html_path}")
            
            print(f"✓ GitHub Pages directory setup: {Path(args.web_output).parent}")
        except Exception as e:
            print(f"✗ Error: {e}", file=sys.stderr)
            sys.exit(1)

    print("\n✓ Done!")


if __name__ == "__main__":
    main()
