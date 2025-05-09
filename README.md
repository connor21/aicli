# Audio Transcription Tool

## Overview
Command line tool for transcribing audio files to text using OpenAI's Whisper model.

## Installation
1. Clone this repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage
To transcribe an audio file:
```bash
python transscribe.py input.mp3 output.txt
```

### Arguments
- `input.mp3`: Path to audio file to transcribe (supports MP3, WAV, etc.)
- `output.txt`: Path to save transcription text

## Dependencies
- Python 3.7+
- whisper
- typer
- moviepy (for audio extraction from video)

## PDF to Markdown Conversion

The tool also includes `pdf2md.py` for converting PDF files to markdown format.

### Usage
```bash
python pdf2md.py input.pdf output.md [--ocr]
```

### Arguments
- `input.pdf`: Path to PDF file to convert  
- `output.md`: Path to save markdown output  
- `--ocr`: Optional flag to enable OCR processing of bitmap content (default: disabled)

### OCR Notes
- When enabled with --ocr, the tool will:
  - Extract text from bitmap images using Tesseract OCR
  - Combine OCR results with regular text extraction
  - May significantly increase processing time

### Examples
```bash
# Convert a PDF to markdown
python pdf2md.py document.pdf converted.md

# Transcribe an audio file
python transscribe.py lecture.mp3 transcript.txt
