import typer
from pathlib import Path
import spacy
from typing import Optional, List
import re
from rapidfuzz import fuzz
import json

app = typer.Typer()

def anonymize_text(
    text: str,
    nlp,
    custom_words: List[str] = None,
    regex_pattern: str = None,
    fuzzy_match: bool = False,
    fuzzy_threshold: int = 85
) -> str:
    """
    Anonymize sensitive information in German text using SpaCy NER and custom rules.

    Args:
        text (str): Input text to anonymize
        nlp: Loaded German SpaCy language model
        custom_words: List of custom words to anonymize
        regex_pattern: Regex pattern for additional matches
        fuzzy_match: Whether to use fuzzy matching for custom words
        fuzzy_threshold: Similarity threshold for fuzzy matches (0-100)

    Returns:
        str: Anonymized text with sensitive entities replaced
    """
    doc = nlp(text)
    anonymized = []
    custom_matches = set()
    
    # Process custom words
    if custom_words:
        if fuzzy_match:
            for word in custom_words:
                for token in doc:
                    similarity = fuzz.ratio(word.lower(), token.text.lower())
                    if similarity >= fuzzy_threshold:
                        custom_matches.add(token.text.lower())
        else:
            custom_matches.update(w.lower() for w in custom_words)
    
    # Process regex matches
    regex_matches = set()
    if regex_pattern:
        regex_matches.update(match.group().lower() for match in re.finditer(regex_pattern, text, re.IGNORECASE))
    
    # Convert text to tokens while preserving original for regex matching
    text_lower = text.lower()
    tokens = [token.text for token in doc]
    
    for i, token in enumerate(tokens):
        token_lower = token.lower()
        if (any(ent.label_ in ["PER", "ORG", "LOC", "DATE"] for ent in doc.ents if ent.start <= i < ent.end) or
            token_lower in custom_matches or
            any(token_lower == m.lower() for m in regex_matches)):
            tokens[i] = "[ANONYMIZIERT]"
    
    return " ".join(tokens)

@app.command()
def anonymize(
    input_file: Path = typer.Argument(..., help="Pfad zur Eingabetextdatei"),
    output_file: Optional[Path] = typer.Argument(None, help="Pfad zur Ausgabedatei (Standard: input_file.anon)"),
    custom_words_file: Optional[Path] = typer.Option(
        None,
        "--custom-words",
        help="JSON-Datei mit Liste von Wörtern zur Anonymisierung"
    ),
    regex_pattern: Optional[str] = typer.Option(
        None,
        "--regex",
        help="Regex-Muster für zusätzliche Anonymisierung"
    ),
    fuzzy_match: bool = typer.Option(
        False,
        "--fuzzy",
        help="Fuzzy-Matching für benutzerdefinierte Wörter aktivieren"
    ),
    fuzzy_threshold: int = typer.Option(
        85,
        "--fuzzy-threshold",
        min=0,
        max=100,
        help="Ähnlichkeitsschwelle für Fuzzy-Matching (0-100)"
    )
):
    """
    Anonymisiert sensible Informationen in einer deutschen Textdatei.
    
    Ersetzt:
    - Benannte Entitäten (Personen, Organisationen, Orte, Daten)
    - Benutzerdefinierte Wörter (optional)
    - Regex-Muster (optional)
    - Ähnliche Wörter bei Fuzzy-Matching (optional)
    """
    if output_file is None:
        output_file = input_file.with_suffix(".anon")
    
    nlp = spacy.load("de_core_news_sm")
    custom_words = None
    
    if custom_words_file:
        with open(custom_words_file, "r", encoding="utf-8") as f:
            custom_words = json.load(f)
    
    with open(input_file, "r", encoding="utf-8") as f:
        text = f.read()
    
    anonymized = anonymize_text(
        text,
        nlp,
        custom_words,
        regex_pattern,
        fuzzy_match,
        fuzzy_threshold
    )
    
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(anonymized)
    
    typer.echo(f"Anonymisierter Text gespeichert in {output_file}")

if __name__ == "__main__":
    app()
