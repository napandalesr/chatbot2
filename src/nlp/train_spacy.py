import spacy
from spacy.training import Example
from spacy.util import minibatch, compounding
from pathlib import Path
import json

# --- Rutas ---
CORPUS_PATH = Path(__file__).parent / "corpus" / "train.jsonl"
MODEL_DIR = Path(__file__).parent / "model-best"

# --- Leer corpus ---
train_data = []
labels_list = [
    "saludo",  # nueva categoría
    "tecnologia_general",
    "tecnologia_especifica",
    "empresa_general",
    "empresa_especifica",
    "idioma_general",
    "idioma_especifico",
    "desconocido"
]

with CORPUS_PATH.open(encoding="utf-8") as f:
    for line in f:
        data = json.loads(line)
        if "text" in data and "labels" in data:
            cats = {label: 1.0 if label in data["labels"] else 0.0 for label in labels_list}
            train_data.append((data["text"], {"cats": cats}))
        else:
            print(f"Línea ignorada por formato inválido: {data}")

# --- Crear pipeline en blanco ---
nlp = spacy.blank("es")

# --- Añadir textcat ---
textcat = nlp.add_pipe("textcat", last=True)
for label in labels_list:
    textcat.add_label(label)

# --- Entrenamiento ---
optimizer = nlp.begin_training()
for epoch in range(10):
    losses = {}
    batches = minibatch(train_data, size=compounding(4.0, 32.0, 1.001))
    for batch in batches:
        examples = []
        for text, annotations in batch:
            doc = nlp.make_doc(text)
            examples.append(Example.from_dict(doc, annotations))
        nlp.update(examples, sgd=optimizer, losses=losses)
    print(f"Epoch {epoch+1}, Losses: {losses}")

# --- Guardar modelo ---
MODEL_DIR.mkdir(exist_ok=True)
nlp.to_disk(MODEL_DIR)
print(f"Modelo guardado en {MODEL_DIR}")
