"""Command line tool to transcribe audio files to text using OpenAI Whisper."""
import typer
from pathlib import Path
import whisper
from pydub import AudioSegment

app = typer.Typer()

@app.command()
def transcribe(
    audio_file: Path = typer.Argument(..., help="Path to audio file to transcribe"),
    output_file: Path = typer.Argument(..., help="Path to save transcription text"),
    start_time: float = typer.Option(None, help="Start time in seconds (optional)"),
    end_time: float = typer.Option(None, help="End time in seconds (optional)"),
):
    """
    Transcribe audio file to text and save results.

    Args:
        audio_file (Path): Path to input audio file
        output_file (Path): Path to save transcription text
        start_time (float): Optional start time in seconds
        end_time (float): Optional end time in seconds
    """
    try:
        # Load audio file
        audio = AudioSegment.from_file(str(audio_file))
        
        # Extract segment if time parameters are specified
        if start_time is not None or end_time is not None:
            start_ms = int((start_time or 0) * 1000)
            end_ms = int((end_time or len(audio)/1000) * 1000)
            audio = audio[start_ms:end_ms]
            
        # Export to temporary file
        temp_file = "temp_audio.wav"
        audio.export(temp_file, format="wav")
        
        # Load whisper model and transcribe
        model = whisper.load_model("base")
        result = model.transcribe(temp_file, fp16=False)
        
        # Clean up temporary file
        Path(temp_file).unlink(missing_ok=True)
        
        # Save transcription
        with open(output_file, "w") as f:
            f.write(result["text"])
            
        typer.echo(f"Successfully transcribed to {output_file}")
        
    except Exception as e:
        typer.echo(f"Error: {str(e)}", err=True)
        raise typer.Exit(1)

if __name__ == "__main__":
    app()
