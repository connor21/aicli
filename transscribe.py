"""Command line tool to transcribe audio files to text using OpenAI Whisper."""
import typer
from pathlib import Path
import whisper

app = typer.Typer()

@app.command()
def transcribe(
    audio_file: Path = typer.Argument(..., help="Path to audio file to transcribe"),
    output_file: Path = typer.Argument(..., help="Path to save transcription text"),
):
    """
    Transcribe audio file to text and save results.

    Args:
        audio_file (Path): Path to input audio file
        output_file (Path): Path to save transcription text
    """
    try:
        # Load whisper model
        model = whisper.load_model("base")
        
        # Transcribe audio
        result = model.transcribe(str(audio_file))
        
        # Save transcription
        with open(output_file, "w") as f:
            f.write(result["text"])
            
        typer.echo(f"Successfully transcribed to {output_file}")
        
    except Exception as e:
        typer.echo(f"Error: {str(e)}", err=True)
        raise typer.Exit(1)

if __name__ == "__main__":
    app()
