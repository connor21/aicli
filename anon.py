import typer
from pathlib import Path
import spacy
from typing import Optional

app = typer.Typer()

def anonymize_text(text: str, nlp) -> str:
    """
    Anonymize sensitive information in German text using SpaCy NER.

    Args:
        text (str): Input text to anonymize
        nlp: Loaded German SpaCy language model

    Returns:
        str: Anonymized text with sensitive entities replaced
    """
    doc = nlp(text)
    anonymized = []
    
    for token in doc:
        if token.ent_type_ in ["PER", "ORG", "LOC", "DATE"]:  # German entity types
            anonymized.append(f"[{token.ent_type_}]")
        else:
            anonymized.append(token.text)
    
    return " ".join(anonymized)

@app.command()
def anonymize(
    input_file: Path = typer.Argument(..., help="Pfad zur Eingabetextdatei"),
    output_file: Optional[Path] = typer.Argument(None, help="Pfad zur Ausgabedatei (Standard: input_file.anon)"),
):
    """
    Anonymisiert sensible Informationen in einer deutschen Textdatei.
    
    Ersetzt benannte Entitäten wie Personen, Organisationen, Orte und Daten
    mit anonymisierten Markierungen.
    """
    if output_file is None:
        output_file = input_file.with_suffix(".anon")
    
    nlp = spacy.load("de_core_news_sm")
    
    with open(input_file, "r", encoding="utf-8") as f:
        text = f.read()
    
    anonymized = anonymize_text(text, nlp)
    
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(anonymized)
    
    typer.echo(f"Anonymisierter Text gespeichert in {output_file}")

if __name__ == "__main__":
    app()
