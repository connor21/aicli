# aicli - Project Planning

## Project Overview
A Collection of command line tools to utilize AI tools.
## Architecture
- **Audio Extraction**: MoviePy
- **Audio to Text**:openai-whisper
- **CLI**:Typer

## Components
1. **TRANSSCRIBE**
   - CLI to transscribe audio files to text
 
## Environment Configuration

## File Structure
```
vsentiment/
├── transscribe.py         # Command line tool to transscribe audio to text
├── pdf2md.py              # conver pd to markdown
├── requirements.txt       # Python dependencies
├── README.md              # Project documentation
├── PLANNING.md            # Project planning (this file)
└── TASK.md                # Task tracking
```

## Style Guidelines
- Follow PEP8 standards
- Use type hints for all functions
- Document functions with Google-style docstrings
- Format code with Black
- Use Pydantic for data validation

## Dependencies
- whisper
- moviepie
- typer
