# 🧠 OpenAI Streamlit Reasoner

Sistema LLM de razonamiento multi-agente desarrollado en Python con **Streamlit** y **OpenAI API**.

Cada consulta compleja es resuelta por múltiples agentes especializados (matemático, lógico, creativo) y luego compaginada por un agente coordinador.

---

## 📂 Estructura del Proyecto

```
├── agents.py         # Definición de agentes y token counter
├── orchestrator.py    # Coordinación de agentes
├── examples.py        # Preguntas de ejemplo
├── main.py            # Aplicación principal en Streamlit
├── README.md          
```

---

## 🚀 Requisitos

- Python 3.10+
- Paquetes:
  - `openai`
  - `streamlit`
  - `pandas`
  - `python-dotenv`

Instalación rápida:

```bash
pip install -r requirements.txt
```

---

## 🔧 Configuración

1. **Clave API de OpenAI**:

   Crea un archivo `.env` en la raíz del proyecto:

   ```bash
   OPENAI_API_KEY=tu-clave-secreta
   ```

2. **Modelos disponibles**:

   Puedes seleccionar entre:

   - `gpt-4.1`
   - `gpt-4.1-mini`
   - `gpt-4o`
   - `gpt-3.5-turbo`

3. **Modos de razonamiento**:

   - Agentes pueden generar **Razonamiento explícito** antes de dar una respuesta final.

---

## 🏁 Cómo ejecutar

Desde el directorio raíz del proyecto:

```bash
streamlit run main.py
```

Se abrirá automáticamente la aplicación en tu navegador.

---

## 🛠️ Funcionalidades

- Procesamiento distribuido entre múltiples agentes
- Compaginación de respuestas por un agente coordinador
- Visualización de estadísticas de uso de tokens
- Estimación de costos de inferencia
- Ejemplos de consultas listas para usar
- Opción para resetear sesión y reiniciar configuración

---

## 📈 Ejemplos de consultas incluidas

- **Cálculo de estructura circular**
- **Análisis financiero**
- **Problema lógico de habitantes**

Puedes agregar más ejemplos en `examples.py`.

---