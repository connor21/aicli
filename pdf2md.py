#!/usr/bin/env python3
"""
PDF to Markdown converter CLI tool.

Usage:
    pdf2md.py <input_pdf> <output_md>

Converts the input PDF file to markdown format and saves to output file.
"""

import argparse
from pathlib import Path
from pdfminer.high_level import extract_text
import re

def convert_pdf_to_markdown(pdf_path: Path, md_path: Path) -> None:
    """Convert PDF file to markdown format and save to output path."""
    # Extract text from PDF
    text = extract_text(pdf_path)
    
    # Basic formatting conversions
    markdown = text
    
    # Convert headings (assuming they're in all caps or have numbers)
    markdown = re.sub(r'\n([A-Z0-9][A-Z0-9 ]+)\n', r'\n# \1\n', markdown)
    
    # Convert bullet points
    markdown = re.sub(r'•\s+', '- ', markdown)
    
    # Remove excessive newlines
    markdown = re.sub(r'\n{3,}', '\n\n', markdown)
    
    # Save to output file
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(markdown)

def main():
    parser = argparse.ArgumentParser(description='Convert PDF to Markdown')
    parser.add_argument('input_pdf', type=Path, help='Input PDF file path')
    parser.add_argument('output_md', type=Path, help='Output markdown file path')
    args = parser.parse_args()

    if not args.input_pdf.exists():
        print(f"Error: Input file {args.input_pdf} does not exist")
        return

    try:
        convert_pdf_to_markdown(args.input_pdf, args.output_md)
        print(f"Successfully converted {args.input_pdf} to {args.output_md}")
    except Exception as e:
        print(f"Error during conversion: {e}")

if __name__ == '__main__':
    main()
