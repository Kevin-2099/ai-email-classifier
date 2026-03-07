import gradio as gr
import re
import json
import csv
import os
from datetime import datetime

from transformers import pipeline
from sentence_transformers import SentenceTransformer, util
from langdetect import detect
import PyPDF2

# -----------------------------
# MODELOS NLP
# -----------------------------
summarizer = pipeline("summarization")
embedding_model = SentenceTransformer(
    "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
    device="cpu"
)

# -----------------------------
# CATEGORÍAS SEMÁNTICAS
# -----------------------------
CATEGORIES = {
    "Urgente": "email crítico que requiere acción inmediata o resolución rápida",
    "Importante pero no urgente": "email relevante de trabajo que necesita revisión posterior",
    "Spam/Promoción": "email publicitario, marketing o venta",
    "Informativo": "email informativo sin necesidad de acción inmediata"
}
category_embeddings = embedding_model.encode(list(CATEGORIES.values()), convert_to_tensor=True)

# -----------------------------
# KEYWORDS INTELIGENTES
# -----------------------------
KEYWORDS = {
    "Urgente": ["urgente", "asap", "crítico", "error", "fallo"],
    "Spam/Promoción": ["oferta", "discount", "promo", "suscríbete"]
}
NEGATIONS = ["no", "not", "never", "sin", "jamás"]

def has_negation(text, keyword, window=4):
    words = re.sub(r"[.,;!?]", " ", text.lower()).split()
    for i, w in enumerate(words):
        if w == keyword.lower():
            start = max(0, i - window)
            context = words[start:i]
            if any(n in context for n in NEGATIONS):
                return True
    return False

# -----------------------------
# HISTORIAL
# -----------------------------
HISTORY_JSON = "email_history.json"
HISTORY_CSV = "email_history.csv"

def save_history(record):
    # JSON completo
    if not os.path.exists(HISTORY_JSON):
        with open(HISTORY_JSON, "w") as f:
            json.dump([], f)
    with open(HISTORY_JSON, "r+") as f:
        data = json.load(f)
        data.append(record)
        f.seek(0)
        json.dump(data, f, indent=2)

    # CSV limpio: reemplaza saltos de línea por espacios
    record_to_csv = record.copy()
    record_to_csv["summary"] = record_to_csv["summary"].replace("\n", " ")
    record_to_csv["full_text"] = record_to_csv["full_text"].replace("\n", " ")

    file_exists = os.path.isfile(HISTORY_CSV)
    with open(HISTORY_CSV, "a", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(
            csvfile,
            fieldnames=record_to_csv.keys(),
            quoting=csv.QUOTE_ALL
        )
        if not file_exists:
            writer.writeheader()
        writer.writerow(record_to_csv)

def download_history():
    if not os.path.exists(HISTORY_JSON):
        return None, None
    return HISTORY_CSV, HISTORY_JSON

# -----------------------------
# PDF ANALYSIS
# -----------------------------
def extract_pdf_text(file):
    if file is None:
        return ""
    text = ""
    reader = PyPDF2.PdfReader(file.name)
    for page in reader.pages:
        if page.extract_text():
            text += page.extract_text() + "\n"
    return text

# -----------------------------
# DETECCIÓN IDIOMA
# -----------------------------
def detect_language(text):
    try:
        return detect(text)
    except:
        return "unknown"

# -----------------------------
# CLASIFICACIÓN SEMÁNTICA
# -----------------------------
def semantic_classification(text):
    text_embedding = embedding_model.encode(text, convert_to_tensor=True)
    scores = util.cos_sim(text_embedding, category_embeddings)[0]
    best_idx = scores.argmax().item()
    return list(CATEGORIES.keys())[best_idx]

# -----------------------------
# KEYWORD BOOST
# -----------------------------
def keyword_boost(text, category):
    text_lower = text.lower()
    for cat, words in KEYWORDS.items():
        for w in words:
            if w in text_lower and not has_negation(text_lower, w):
                return cat, f"Keyword detectada: '{w}'"
    return category, "Clasificación basada en embeddings semánticos"

# -----------------------------
# RESUMEN ROBUSTO
# -----------------------------
def safe_summary(text):
    if len(text.split()) < 40:
        return text[:150]
    try:
        return summarizer(text[:1000], max_length=80, min_length=25, do_sample=False)[0]["summary_text"]
    except:
        return text[:150]

# -----------------------------
# FUNCIÓN PRINCIPAL
# -----------------------------
def classify_email(email_text, attachment):
    attachment_text = extract_pdf_text(attachment)
    full_text = email_text + "\n" + attachment_text
    language = detect_language(full_text)
    category = semantic_classification(full_text)
    category, explanation = keyword_boost(full_text, category)
    summary = safe_summary(full_text)

    record = {
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "language": language,
        "category": category,
        "summary": summary,
        "full_text": full_text,
        "attachment": bool(attachment)
    }
    save_history(record)

    html_output = f"""
    <div style='border:2px solid #4CAF50; padding:20px; border-radius:12px; background:#f9f9f9'>
        <h2>📧 Email AI Analysis</h2>
        <p><b>Idioma:</b> {language}</p>
        <p><b>Categoría:</b> {category}</p>
        <h4>Resumen</h4>
        <p>{summary}</p>
        <h4>Explicación</h4>
        <p>{explanation}</p>
    </div>
    """
    return html_output

# -----------------------------
# HISTORIAL VISUAL CON CONTENIDO COMPLETO
# -----------------------------
def load_history():
    if not os.path.exists(HISTORY_JSON):
        return "Sin historial todavía."
    with open(HISTORY_JSON) as f:
        data = json.load(f)

    html = "<h3>📊 Historial de Emails (últimos 10)</h3>"
    for idx, r in enumerate(reversed(data[-10:])):
        html += f"""
        <div style='border:1px solid gray;margin:5px;padding:10px'>
            <b>{r['date']} | {r['category']}</b>
            <button onclick="document.getElementById('full_{idx}').style.display='block'">Ver contenido completo</button>
            <div id='full_{idx}' style='display:none; margin-top:10px; white-space: pre-wrap; border-top:1px solid #ccc; padding-top:5px;'>
                {r['full_text']}
            </div>
        </div>
        """
    return html

# -----------------------------
# INTERFAZ GRADIO
# -----------------------------
with gr.Blocks() as demo:
    gr.Markdown("# 🤖 AI Email Classifier")

    email_input = gr.Textbox(lines=10, label="Email")
    attachment = gr.File(label="Adjunto PDF (opcional)")
    output = gr.HTML()

    analyze_btn = gr.Button("Analizar Email")
    history_btn = gr.Button("Ver Historial")
    download_btn = gr.Button("Descargar Historial")
    csv_file = gr.File(label="CSV")
    json_file = gr.File(label="JSON")

    analyze_btn.click(classify_email, inputs=[email_input, attachment], outputs=output)
    history_btn.click(load_history, outputs=output)
    download_btn.click(download_history, inputs=None, outputs=[csv_file, json_file])

if __name__ == "__main__":
    demo.launch()
