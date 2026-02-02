#!/usr/bin/env python3
"""
CV Generator - Publications section regeneration
Only handles updating the Publications section from bibliography.bib
"""

from pathlib import Path
from typing import Dict, List, Any
from bibtexparser import load as load_bibtex
from bibtexparser.bparser import BibTexParser
from bibtexparser.customization import convert_to_unicode


class CVGenerator:
    """Class for regenerating Publications section from bibliography"""
    
    def __init__(self, bib_path: str = "bibliography.bib", cv_path: str = "cv.md"):
        self.bib_path = Path(bib_path)
        self.cv_path = Path(cv_path)
        
    def parse_bibliography(self) -> List[Dict[str, Any]]:
        """Parse bibliography.bib and return publications ordered by date"""
        with open(self.bib_path, 'r', encoding='utf-8') as f:
            parser = BibTexParser()
            parser.customization = convert_to_unicode
            bib_database = load_bibtex(f, parser=parser)
        
        publications = []
        
        for entry in bib_database.entries:
            pub = {
                'entry_type': entry.get('ENTRYTYPE', ''),
                'title': entry.get('title', ''),
                'author': entry.get('author', ''),
                'year': entry.get('year', ''),
                'month': entry.get('month', ''),
                'journal': entry.get('journal', ''),
                'booktitle': entry.get('booktitle', ''),
                'pages': entry.get('pages', ''),
                'doi': entry.get('doi', ''),
                'url': entry.get('url', ''),
                'publisher': entry.get('publisher', ''),
            }
            
            # Create date for sorting (use year-month-day if available)
            year = int(pub['year']) if pub['year'] else 0
            month_map = {
                'jan': 1, 'feb': 2, 'mar': 3, 'apr': 4, 'may': 5, 'jun': 6,
                'jul': 7, 'aug': 8, 'sep': 9, 'oct': 10, 'nov': 11, 'dec': 12
            }
            month = month_map.get(pub['month'].lower()[:3] if pub['month'] else '', 0)
            day = int(entry.get('day', 1)) if entry.get('day') else 1
            
            pub['sort_date'] = (year, month, day)
            publications.append(pub)
        
        # Sort by date (newest first)
        publications.sort(key=lambda x: x['sort_date'], reverse=True)
        
        return publications
    
    def clean_latex(self, text: str) -> str:
        """Remove LaTeX escape sequences from text and escape special characters for PDF"""
        if not text:
            return text
        
        # Handle LaTeX ampersand commands in various forms
        # First handle math mode: $\&$ -> &
        text = text.replace('$\\&$', '&')
        # Handle escaped ampersand: \& -> &
        text = text.replace('\\&', '&')
        # Handle math mode without escape: $&$ -> & (after backslash removal)
        
        # Remove other LaTeX escapes (but keep the text)
        text = text.replace('\\', '')
        
        # Now handle any remaining $&$ patterns (after backslash removal)
        text = text.replace('$&$', '&')
        
        # Remove curly braces used for LaTeX grouping
        text = text.replace('{', '').replace('}', '')
        
        # Remove dollar signs (math mode delimiters)
        text = text.replace('$', '')
        
        # Escape ampersand for LaTeX/PDF output (pandoc will convert &amp; to \& in LaTeX)
        text = text.replace('&', '&amp;')
        
        return text
    
    def format_publication(self, pub: Dict[str, Any]) -> str:
        """Format a single publication entry for markdown"""
        # Format authors
        authors = pub.get('author', '')
        if authors:
            authors = self.clean_latex(authors)
            authors = authors.replace(' and ', ' and ')
        
        # Format date
        date_parts = []
        if pub.get('month'):
            month = pub['month'][:3].capitalize()
            date_parts.append(month)
        if pub.get('year'):
            date_parts.append(pub['year'])
        date_str = ' '.join(date_parts) if date_parts else ''
        
        # Format venue
        venue = pub.get('journal') or pub.get('booktitle') or pub.get('publisher', '')
        if venue:
            venue = self.clean_latex(venue)
        
        # Format title
        title = pub.get('title', '')
        if title:
            title = self.clean_latex(title)
            title = f'"{title}"'
        
        # Build citation
        parts = []
        if authors:
            parts.append(authors)
        if date_str:
            parts.append(f'({date_str})')
        if title:
            parts.append(title)
        if venue:
            parts.append(f'In: {venue}')
        if pub.get('pages'):
            parts.append(f'pp. {pub["pages"]}')
        if pub.get('doi'):
            parts.append(f'doi: {pub["doi"]}')
        if pub.get('url'):
            parts.append(f'url: {pub["url"]}')
        
        return '. '.join(parts) + '.'
    
    def generate_publications_section(self, language: str = "en") -> str:
        """Generate publications section from bibliography
        
        Args:
            language: Language code ('en' for English, 'es' for Spanish)
        """
        publications = self.parse_bibliography()
        
        if language == "es":
            section_header = "## Publicaciones"
            no_pubs_msg = "No se encontraron publicaciones.\n"
        else:
            section_header = "## Publications"
            no_pubs_msg = "No publications found.\n"
        
        if not publications:
            return f"{section_header}\n\n{no_pubs_msg}"
        
        section = f"{section_header}\n\n"
        for pub in publications:
            section += "* " + self.format_publication(pub) + "\n"
        
        return section
    
    def regenerate_publications(self) -> str:
        """Regenerate Publications section in the CV (auto-detects language)"""
        if not self.cv_path.exists():
            raise FileNotFoundError(f"CV file not found: {self.cv_path}")
        
        # Read current CV
        with open(self.cv_path, 'r', encoding='utf-8') as f:
            cv_content = f.read()
        
        # Detect language by checking which section header exists
        pub_start_en = cv_content.find('## Publications')
        pub_start_es = cv_content.find('## Publicaciones')
        
        if pub_start_en != -1:
            language = "en"
            section_header = "## Publications"
            pub_start = pub_start_en
        elif pub_start_es != -1:
            language = "es"
            section_header = "## Publicaciones"
            pub_start = pub_start_es
        else:
            raise ValueError("Publications/Publicaciones section not found in CV")
        
        # Generate new publications section
        publications_section = self.generate_publications_section(language=language)
        
        # Find the end of the publications section (next ## or ```)
        remaining = cv_content[pub_start + len(section_header):]
        next_section = remaining.find('\n## ')
        next_code = remaining.find('\n```')
        
        # Determine where the publications section ends
        if next_section != -1 and next_code != -1:
            end_pos = min(next_section, next_code)
        elif next_section != -1:
            end_pos = next_section
        elif next_code != -1:
            end_pos = next_code
        else:
            end_pos = len(remaining)
        
        # Replace the publications section
        new_cv = (cv_content[:pub_start] + 
                 publications_section.rstrip() + '\n\n' + 
                 cv_content[pub_start + len(section_header) + end_pos:])
        
        # Write updated CV
        with open(self.cv_path, 'w', encoding='utf-8') as f:
            f.write(new_cv)
        
        return str(self.cv_path)
