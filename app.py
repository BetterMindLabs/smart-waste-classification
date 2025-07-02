import gradio as gr
import google.generativeai as genai
from PIL import Image

# Configure Gemini API key
genai.configure(api_key=st.secrets["API_KEY"])

# Load Gemini vision model
vision_model = genai.GenerativeModel("gemini-2.5-flash")

def classify_waste(image):
    prompt = """
Classify the waste item in this image into one of these categories:
1. Recyclable
2. Compostable
3. General waste (non-recyclable)

Also provide a short, practical disposal tip for the user.
"""
    # Call Gemini with prompt + image
    response = vision_model.generate_content([prompt, image])
    result = response.text
    return result

with gr.Blocks(theme=gr.themes.Soft(primary_hue="green")) as demo:
    gr.Markdown(
        """
        # ♻️ **Smart Waste Classifier**
        Upload a photo of your waste item to get an AI-powered classification (Recyclable, Compostable, or General Waste) along with a helpful disposal tip!  
        Let's make sorting easier and greener 🌱.
        """
    )
    
    with gr.Row():
        with gr.Column(scale=1):
            image_input = gr.Image(type="pil", label="Upload Your Waste Image Here 🗑️")
            classify_button = gr.Button("🚀 Classify Waste")
            clear_button = gr.Button("🗑️ Clear")
        with gr.Column(scale=1):
            output_text = gr.Textbox(label="🟢 Result & Tip", lines=10, interactive=False)

    classify_button.click(fn=classify_waste, inputs=image_input, outputs=output_text)
    clear_button.click(lambda: (None, ""), outputs=[image_input, output_text])

    gr.Markdown("---")
    gr.Markdown("✅ **Thank you for contributing to a cleaner world!** 💚")

demo.launch()
