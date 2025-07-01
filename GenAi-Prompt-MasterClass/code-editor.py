import gradio as gr
import google.generativeai as genai

# Setup API key
genai.configure(api_key="AIzaSyD-245NS000wU-Q120s7rwZ5EvarJB4ZLU")  # Replace with your actual Gemini API key

# Load Gemini model
model = genai.GenerativeModel("gemini-1.5-flash")  # Or use "gemini-pro"

def auto_complete(code, language):
    prompt = f"""You are an expert {language} developer.
Continue the following code with proper indentation and logic.

Code so far:
{code}

### Continue code:"""

    try:
        response = model.generate_content(prompt)
        suggestion = response.text.strip() if response.text else ""
        if not suggestion:
            return code + "\n# No suggestion returned"
        return code + "\n" + suggestion
    except Exception as e:
        return code + f"\n\n# ❌ Error: {e}"

languages = ["python", "javascript", "html", "cpp", "java"]

with gr.Blocks() as demo:
    gr.Markdown("## 🧠 Gemini Auto Code Completion")

    lang = gr.Dropdown(label="Select Language", choices=languages, value="python")
    code_editor = gr.Code(label="Your Code", language="python", interactive=True, lines=20)
    complete_btn = gr.Button("✨ Auto Complete Code")

    complete_btn.click(fn=auto_complete, inputs=[code_editor, lang], outputs=code_editor)
    lang.change(lambda l: gr.update(language=l), inputs=lang, outputs=code_editor)

demo.launch()
