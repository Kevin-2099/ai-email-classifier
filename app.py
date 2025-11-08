# app.py (versión con tarjeta visual)
import gradio as gr
from transformers import pipeline
import re

# -----------------------------
# Pipelines
# -----------------------------
classifier = pipeline("text-classification", model="distilbert-base-uncased-finetuned-sst-2-english")
sentiment_analyzer = pipeline("sentiment-analysis")
summarizer = pipeline("summarization")

# -----------------------------
# Palabras clave
# -----------------------------
KEYWORDS = {
    "Urgente": ["urgente", "inmediato", "crítico", "fallo", "problema", "atención"],
    "Importante pero no urgente": ["importante", "revisar", "feedback", "reunión", "documento", "contrato"],
    "Spam/Promoción": ["oferta", "promoción", "suscríbete", "compra", "descuento", "gana dinero", "ahora"],
    "Informativo": ["informativo", "recordatorio", "notificación", "aviso", "resumen"]
}
CONTEXT_KEYWORDS = {
    "Urgente": [["responder", "urgente"], ["atención", "inmediato"]],
}
NEGATION_WORDS = ["no", "sin", "nunca", "jamás"]

# -----------------------------
# Funciones auxiliares
# -----------------------------
def has_negation_robust(text, keyword, window=5):
    text_clean = re.sub(r'[.,;!?]', ' ', text.lower())
    words = text_clean.split()
    for i, w in enumerate(words):
        if w == keyword.lower():
            start = max(0, i - window)
            context = words[start:i]
            if any(neg in context for neg in NEGATION_WORDS):
                return True
    return False

def check_context(text, keyword):
    text_clean = re.sub(r'[.,;!?]', ' ', text.lower())
    words = text_clean.split()
    for ctx_pair in CONTEXT_KEYWORDS.get("Urgente", []):
        if keyword in ctx_pair:
            if all(word in words for word in ctx_pair):
                return True
            else:
                return False
    return True

# -----------------------------
# Función principal
# -----------------------------
def classify_email(email_text):
    text_lower = email_text.lower()
    
    # Clasificación por keywords
    for category, words in KEYWORDS.items():
        for word in words:
            if re.search(r"\b" + re.escape(word) + r"\b", text_lower):
                if has_negation_robust(email_text, word):
                    continue
                if not check_context(email_text, word):
                    continue
                explanation = f"Se detectó la palabra clave '{word}' asociada con la categoría '{category}'."
                break
        else:
            continue
        break
    else:
        # Fallback modelo
        pred = classifier(email_text)[0]
        label = pred['label']
        score = pred['score']

        if label == 'NEGATIVE' and score > 0.7:
            category = "Urgente"
            explanation = "El contenido del email sugiere urgencia según el modelo."
        elif label == 'POSITIVE' and score > 0.7:
            category = "Importante pero no urgente"
            explanation = "El email es relevante pero no urgente según el modelo."
        else:
            category = "Informativo"
            explanation = "El email parece ser solo informativo según el modelo."

    # Tono
    sentiment = sentiment_analyzer(email_text)[0]
    tone = f"{sentiment['label']} ({sentiment['score']:.2f})"

    # Resumen
    try:
        summary = summarizer(email_text, max_length=60, min_length=20, do_sample=False)[0]['summary_text']
    except:
        summary = email_text[:100] + "..."

    # Formato HTML tipo tarjeta
    html_output = f"""
    <div style='border:2px solid #4CAF50; padding:15px; border-radius:10px; max-width:700px; background-color:#f9f9f9;'>
        <h3>📧 Clasificación de Email</h3>
        <p><b>Categoría:</b> {category}</p>
        <p><b>Tono:</b> {tone}</p>
        <p><b>Resumen:</b> {summary}</p>
        <p><b>Explicación:</b> {explanation}</p>
    </div>
    """
    return html_output

# -----------------------------
# Interfaz Gradio
# -----------------------------
iface = gr.Interface(
    fn=classify_email,
    inputs=gr.Textbox(lines=10, placeholder="Pega aquí el email..."),
    outputs=gr.HTML(),  # Mostrar HTML en tarjeta
    title="Clasificador de Emails",
    description="Clasifica emails en: Urgente, Importante, Informativo, Spam. Además detecta el tono y genera un resumen automático en tarjeta visual."
)

if __name__ == "__main__":
    iface.launch()
