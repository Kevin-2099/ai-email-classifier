# 🤖 AI Email Classifier

Clasificador inteligente de correos electrónicos basado en IA semántica, capaz de analizar emails y PDFs, generar resúmenes automáticos y mantener un historial exportable. Ideal como MVP para productividad y soporte técnico.

## 📧 Categorías Detectadas

- 🔴 Urgente — requiere acción inmediata

- 🟡 Importante pero no urgente — revisión posterior

- 📄 Informativo — solo lectura

- 🚫 Spam / Promoción — marketing o publicidad

## ✨ Funcionalidades

- 🧠 Clasificación Semántica: analiza el significado completo usando embeddings multilingües.

- 🔍 Keyword Boost: detecta palabras críticas y evalúa negaciones contextuales.

- 🌍 Detección de idioma automática (multilingüe).

- 📝 Resumen Automático del contenido del email + PDF adjunto.

- 📎 Análisis de PDFs: extracción y clasificación del texto adjunto.

- 📊 Historial Inteligente (últimos 10 emails) con exportación CSV/JSON.

- 🎨 Interfaz Web con Gradio: análisis en un clic y visualización clara.

## 🧱 Stack Tecnológico

- Python 3.10+

- Transformers (Hugging Face)

- Sentence Transformers

- Gradio

- PyPDF2

- langdetect

- Modelos NLP

  - Summarization pipeline
  
  - paraphrase-multilingual-MiniLM-L12-v2 (embeddings semánticos)

## ⚙️ Instalación
git clone https://github.com/Kevin-2099/ai-email-classifier.git

cd ai-email-classifier

pip install -r requirements.txt

python app.py

Se abrirá automáticamente la interfaz web.

## 🚀 Uso

- Pegue el email.

- (Opcional) Suba un PDF.

- Pulse Analizar Email.

- Se mostrará:

  - Idioma detectado
  
  - Categoría
  
  - Resumen automático
  
  - Explicación de la clasificación

## 🧠 Cómo Funciona

- Combina texto del email + PDF

- Detecta idioma automáticamente

- Clasificación semántica con embeddings

- Ajuste mediante keywords y negaciones

- Generación de resumen

- Guardado automático en historial

## 🎯 Casos de Uso

- Automatización de bandeja de entrada

- Helpdesk y soporte técnico

- Priorización automática de emails

- Asistentes AI personales

## 📄 Licencia

Este proyecto se distribuye bajo una **licencia propietaria con acceso al código (source-available)**.

El código fuente se pone a disposición únicamente para fines de **visualización, evaluación y aprendizaje**.

❌ No está permitido copiar, modificar, redistribuir, sublicenciar, ni crear obras derivadas del software o de su código fuente sin autorización escrita expresa del titular de los derechos.

❌ El uso comercial del software, incluyendo su oferta como servicio (SaaS), su integración en productos comerciales o su uso en entornos de producción, requiere un **acuerdo de licencia comercial independiente**.

📌 El texto **legalmente vinculante** de la licencia es la versión en inglés incluida en el archivo `LICENSE`. 

Se proporciona una traducción al español en `LICENSE_ES.md` únicamente con fines informativos. En caso de discrepancia, prevalece la versión en inglés.

## Autor
Kevin-2099
