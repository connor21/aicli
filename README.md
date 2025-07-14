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

To transcribe a specific segment (30s to 90s):
```bash
python transscribe.py input.mp3 output.txt --start-time 30 --end-time 90
```

### Notes:
- Time parameters require ffmpeg to be installed on your system
- Supported audio formats: MP3, WAV, FLAC, etc.
- For large files, processing just a segment can be faster

### Arguments
- `input.mp3`: Path to audio file to transcribe (supports MP3, WAV, etc.)
- `output.txt`: Path to save transcription text
- `--start-time`: Optional start time in seconds (transcribe from this point)
- `--end-time`: Optional end time in seconds (transcribe up to this point)

## Dependencies
- Python 3.7+
- whisper
- typer
- pydub (for audio segment extraction)
- ffmpeg (required by pydub - install via system package manager)
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

## Text Anonymization Tool

The tool includes `anon.py` for anonymizing sensitive information in German text files.

### Usage
```bash
python anon.py input.txt [output.txt] [OPTIONS]
```

### Arguments
- `input.txt`: Path to text file to anonymize
- `output.txt`: Optional output path (default: input.anon)

### Options
- `--custom-words`: Path to JSON file with custom words to anonymize
- `--regex`: Regex pattern for additional matches
- `--fuzzy`: Enable fuzzy matching for custom words
- `--fuzzy-threshold`: Similarity threshold for fuzzy matches (0-100, default: 85)

### Examples
```bash
# Basic anonymization
python anon.py document.txt

# With custom words list
python anon.py document.txt --custom-words sensitive.json

# With regex pattern for phone numbers
python anon.py document.txt --regex "\d{3}-\d{3}-\d{4}"

# With fuzzy matching
python anon.py document.txt --custom-words names.json --fuzzy --fuzzy-threshold 80
```

### Custom Words File Format
Create a JSON file (e.g., sensitive.json) with an array of terms:
```json
[
    "Meier",
    "Müller",
    "Bankverbindung",
    "Krankenkasse"
]
```
