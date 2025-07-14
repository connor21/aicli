
## Current Tasks
- [x] Implement transscribe.py as CLI with an audio file as input parameter and a filename for the result as output
- [x] Implement transscription of audiofile to text
- [x] Implement saving the result to the textfile given as parameter
- [x] create documentation in README.md
- [x] Add requirements.txt

## Implement pdf2md
- [x] implement `pdf2md.py` as a CLI with a pdf as input and a filename for the result as output
- [x] Implement conversion of the input PDF file to markdown
- [x] Implement saving the result to the file given as parameter
- [x] update documentation in README.md
- [x] update requirements.txt

## Implement OCR
- [x] implement OCR to convert bitmap data to text in `pdf2md.py`
- [x] Add OCR result to output file
- [x] Add parameter to `pdf2md.py` enable OCR or disable OCR extraction - default is disable OCR extraction

## Implement Anonymization

- [x] implement anonymization for text in `anon.py`
- [x] extend `anon.py` to support a custom word list and regular expressions to find words that should be anonymized
- [x] Add fuzzy matching option using rapidfuzz for similar words

## Implement time parameter in `transscribe.py`

- [x] support start and end time for the transscription. Only the time in the input file defined by start and end is transscribed. If the parameter are not set, the cmolete file is transcribed.
