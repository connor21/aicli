#!/usr/bin/env python3
"""
PDF to Markdown converter CLI tool.

Usage:
    pdf2md.py <input_pdf> <output_md>

Converts the input PDF file to markdown format and saves to output file.
Handles both text and bitmap content using OCR.
"""

import argparse
from pathlib import Path
from pdfminer.high_level import extract_text
from pdf2image import convert_from_path
import pytesseract
from PIL import Image, ImageEnhance
import re
import tempfile

def extract_text_with_ocr(pdf_path: Path) -> str:
    """Extract text from PDF including OCR for bitmap content."""
    # First get text from PDFMiner
    text = extract_text(pdf_path)
    print(f"PDFMiner extracted {len(text)} characters")
    
    # Then extract images and perform OCR
    with tempfile.TemporaryDirectory() as temp_dir:
        try:
            # Process pages one at a time to avoid file handle exhaustion
            page_count = 1
            while True:
                images = convert_from_path(pdf_path, 
                                        output_folder=temp_dir,
                                        first_page=page_count,
                                        last_page=page_count)
                if not images:
                    break
                    
                image = images[0]
                try:
                    print(f"Processing page {page_count} with dimensions {image.size}")
                    # Convert to grayscale for better OCR
                    gray_image = image.convert('L')
                    # Increase contrast
                    enhancer = ImageEnhance.Contrast(gray_image)
                    enhanced = enhancer.enhance(2.0)
                    
                    ocr_text = pytesseract.image_to_string(enhanced, 
                                                         config='--psm 6 --oem 3')
                    print(f"Page {page_count} OCR extracted {len(ocr_text)} characters")
                    text += f"\n\n[OCR Result Page {page_count}]\n{ocr_text}"
                    page_count += 1
                finally:
                    if 'image' in locals():
                        image.close()
        except Exception as e:
            print(f"Warning: OCR processing failed - {e}")
            import traceback
            traceback.print_exc()
    
    return text

def convert_pdf_to_markdown(pdf_path: Path, md_path: Path, use_ocr: bool = False) -> None:
    """Convert PDF file to markdown format and save to output path."""
    # Extract text with optional OCR
    text = extract_text_with_ocr(pdf_path) if use_ocr else extract_text(pdf_path)
    
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
    parser.add_argument('--ocr', action='store_true', 
                      help='Enable OCR processing of bitmap content (default: disabled)')
    args = parser.parse_args()

    if not args.input_pdf.exists():
        print(f"Error: Input file {args.input_pdf} does not exist")
        return

    try:
        convert_pdf_to_markdown(args.input_pdf, args.output_md, args.ocr)
        print(f"Successfully converted {args.input_pdf} to {args.output_md}")
    except Exception as e:
        print(f"Error during conversion: {e}")

if __name__ == '__main__':
    main()
