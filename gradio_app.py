import gradio as gr
import os
from dotenv import load_dotenv

from brain_of_the_doctor import encode_image, analyze_image_with_query
from voice_of_the_patient import transcribe_with_groq
from voice_of_the_doctor import text_to_speech_with_gtts

load_dotenv()

system_prompt = """You have to act as a professional doctor... (your full prompt here)"""

def process_inputs(audio_filepath, image_filepath):
    transcript = transcribe_with_groq(
        GROQ_API_KEY=os.environ.get("GROQ_API_KEY"),
        audio_filepath=audio_filepath,
        stt_model="whisper-large-v3"
    )

    if image_filepath:
        doctor_response = analyze_image_with_query(
            query=system_prompt + transcript,
            encoded_image=encode_image(image_filepath),
            model="meta-llama/llama-4-scout-17b-16e-instruct"
        )
    else:
        doctor_response = "No image provided for me to analyze."

    voice_path = text_to_speech_with_gtts(
        input_text=doctor_response,
        output_filepath="final.mp3"
    )

    return transcript, doctor_response, voice_path

# ✅ Valid theme with medical blue and white background
medical_theme = gr.themes.Base(
    primary_hue="blue",
    neutral_hue="gray",
    font=["Helvetica", "Arial", "sans-serif"]
)

# 🩺 Gradio UI Layout
with gr.Blocks(title="VocDoc | AI Medical Assistant", theme=medical_theme, css=".gradio-container { background-color: #ffffff !important; }") as demo:
    gr.Markdown(
        """
        <h1 style='color:#007BFF;'>🩺 VocDoc – Voice & Vision Powered AI Doctor</h1>
        <p style='font-size:16px;'>Upload a medical image and speak your symptoms — VocDoc listens, sees, and responds like a human doctor using AI.</p>
        """
    )


    with gr.Row():
        with gr.Column():
            audio_input = gr.Audio(sources=["microphone"], type="filepath", label="🎤 Speak your symptoms")
            image_input = gr.Image(type="filepath", label="🖼️ Upload medical image (e.g., skin issue)")
            submit_btn = gr.Button("🩺 Get Diagnosis", variant="primary")

        with gr.Column():
            transcript_output = gr.Textbox(label="📝 Transcribed Symptoms", lines=3)
            response_output = gr.Textbox(label="👩‍⚕️ Doctor's Response", lines=5)
            audio_output = gr.Audio(label="🔊 Voice Response")

    submit_btn.click(
        fn=process_inputs,
        inputs=[audio_input, image_input],
        outputs=[transcript_output, response_output, audio_output]
    )

demo.launch(debug=True)
