# flask app

from flask import Flask, jsonify, request
from modules.gemini_interface import make_summary, make_script, pdf_to_text, generate_initial_image
from modules.runway_interface import generate_video
import asyncio

app = Flask(__name__)

@app.route('/api/pdf_to_text', methods=['POST'])
def api_pdf_to_text():
    data = request.get_json()
    file_path = data.get("file_path")

    if not file_path:
        return jsonify({"error": "File path missing"}), 400

    try:
        pdf_to_text(file_path)
        return jsonify({"message": "Text extracted and saved to data/text.txt"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/api/make_summary', methods=['POST'])
def api_make_summary():
    data = request.get_json()
    text = data.get("text")

    if not text:
        return jsonify({"error": "Text missing"}), 400

    try:
        summary = make_summary(text)
        return jsonify({"summary": summary})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/api/make_script', methods=['POST'])
def api_make_script():
    data = request.get_json()
    summary = data.get("summary")

    if not summary:
        return jsonify({"error": "Summary missing"}), 400

    try:
        script = make_script(summary)
        return jsonify({"script": script})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/api/generate_initial_image', methods=['POST'])
def api_generate_initial_image():
    data = request.get_json()
    script = data.get("script")

    if not script:
        return jsonify({"error": "Script missing"}), 400

    try:
        image_path = generate_initial_image(script)
        return jsonify({"image_path": image_path})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

@app.route('/api/generate_video', methods=['POST'])
def api_generate_video():
    data = request.get_json()
    prompt_text = data.get("prompt_text")
    prompt_image = data.get("prompt_image")  # Retrieve the prompt_image from request

    if not prompt_text or not prompt_image:
        return jsonify({"error": "Prompt text or prompt image missing"}), 400

    # Run the async function within Flask's synchronous request
    try:
        video_id = asyncio.run(generate_video(prompt_text, prompt_image))
        return jsonify({"video_id": video_id})
    except Exception as e:
        return jsonify({"error": str(e)}), 500




