from flask import Flask, jsonify, request, send_file
from modules.gemini_interface import (
    make_summary, make_script, pdf_to_text, generate_initial_image,
    generate_captions, create_srt, burn_subtitles
)
from modules.runway_interface import generate_videos, stitch_videos
import asyncio
import os
import threading

app = Flask(__name__)

BASE_PATH = "/react-flask-app/data/"

processing_tasks = {}

# Route to handle PDF upload and start processing
@app.route('/upload_pdf', methods=['POST'])
def upload_pdf():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file:
        # Save the uploaded file
        file_path = os.path.join(BASE_PATH, "books", file.filename)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        file.save(file_path)

        output_filename = f"{os.path.splitext(file.filename)[0]}_captioned_trailer.mp4"
        output_path = os.path.join(BASE_PATH, output_filename)

        # Start processing in a new thread
        task_id = file.filename  
        processing_tasks[task_id] = 'processing'

        threading.Thread(target=process_file, args=(file_path, output_path, task_id)).start()

        return jsonify({"message": "Processing started", "task_id": task_id}), 202

    return jsonify({"error": "Something went wrong"}), 500

def process_file(file_path, output_path, task_id):
    try:
        text = pdf_to_text(file_path)
        summary = make_summary(text)
        script = make_script(summary)
        videos = asyncio.run(generate_videos(script, os.path.join(BASE_PATH, "images")))
        trailer = stitch_videos(videos, os.path.join(BASE_PATH, "output.mp4"))
        captions = generate_captions(script)
        srt = create_srt(captions)
        captioned_trailer = burn_subtitles(trailer, srt, output_path)
        processing_tasks[task_id] = 'completed'
    except Exception as e:
        processing_tasks[task_id] = f'error: {str(e)}'
        print(f"Error processing task {task_id}: {e}")

# Route to check processing status
@app.route('/status/<task_id>', methods=['GET'])
def check_status(task_id):
    status = processing_tasks.get(task_id, 'not found')
    return jsonify({"status": status}), 200

# Route to download the final video
@app.route('/download/<task_id>', methods=['GET'])
def download_file(task_id):
    output_filename = f"{os.path.splitext(task_id)[0]}_captioned_trailer.mp4"
    output_path = os.path.join(BASE_PATH, output_filename)

    if os.path.exists(output_path):
        return send_file(output_path, as_attachment=True)
    else:
        return jsonify({"error": "File not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
