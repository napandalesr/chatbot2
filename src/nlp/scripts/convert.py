import srsly
import spacy
from spacy.tokens import DocBin

def convert(input_file, output_file):
    nlp = spacy.blank("es")
    db = DocBin()

    for example in srsly.read_jsonl(input_file):
        doc = nlp.make_doc(example["text"])
        doc.cats = {
            "tecnologia_general": 1.0 if example["label"] == "tecnologia_general" else 0.0,
            "tecnologia_especifica": 1.0 if example["label"] == "tecnologia_especifica" else 0.0,
            "empresa_general": 1.0 if example["label"] == "empresa_general" else 0.0,
            "empresa_especifica": 1.0 if example["label"] == "empresa_especifica" else 0.0,
            "idioma_general": 1.0 if example["label"] == "idioma_general" else 0.0,
            "idioma_especifico": 1.0 if example["label"] == "idioma_especifico" else 0.0,
            "desconocido": 1.0 if example["label"] == "desconocido" else 0.0
        }
        db.add(doc)

    db.to_disk(output_file)
    print(f"Saved {output_file}")

convert("/app/nlp/corpus/train.jsonl", "/app/nlp/training/train.spacy")
convert("/app/nlp/corpus/dev.jsonl", "/app/nlp/training/dev.spacy")
