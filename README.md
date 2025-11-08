# 📧 Clasificador de Emails con IA

Este proyecto es una herramienta inteligente de clasificación de correos electrónicos desarrollada con Python, Hugging Face y Gradio. 
Analiza el texto del correo electrónico y lo clasifica en una de las siguientes categorías, además de proporcionar detección de tono y un resumen automático:

- 🟥 **Urgente** (requiere atención inmediata)  
- 🟨 **Importante pero no urgente**  
- 🟦 **Informativo**  
- 🟩 **Spam / Promoción**  

---

## 🚀 Tecnologías utilizadas
- Transformers (Hugging Face) → modelos:

- distilbert-base-uncased-finetuned-sst-2-english (clasificación de texto)

- Proceso de resumen (resumen automático)

- Proceso de análisis de sentimientos (detección de tono)

- Gradio → interfaz web interactiva con salida de tarjetas visuales

- scikit-learn → opcional, para preprocesamiento o entrenamiento futuro
---
## 🧠 Cómo funciona
1. Clasificación basada en reglas
- El sistema busca palabras clave típicas de cada categoría (p. ej., "urgente", "inmediato", "oferta", "recordatorio"). Las reglas de contexto y la detección de negación ayudan a reducir los falsos positivos.

2. Fallback al modelo de cara abrazada
- Si no se encuentran palabras clave claras, el modelo DistilBERT predice la categoría basándose en el contenido del correo electrónico. Esto garantiza que el sistema siempre proporcione una clasificación adecuada.

3. Detección de tonos
- El sistema analiza el sentimiento del correo electrónico (positivo, negativo, neutral) para proporcionar un indicador de tono adicional.

4. Resumen automático
- Se genera automáticamente un breve resumen del contenido del correo electrónico mediante el proceso de resumen.

5. Salida de tarjeta visual
- Los resultados se muestran en una única tarjeta visual con categoría, tono, resumen y explicación, por lo que todo es fácil de leer sin necesidad de desplazarse.
