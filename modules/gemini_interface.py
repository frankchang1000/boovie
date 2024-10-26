import google.generativeai as genai
import os
import requests
from flask import Flask, request, jsonify


genai.configure(api_key=os.environ["API_KEY"])
model = genai.GenerativeModel("gemini-1.5-flash")



def extract_text(pdf):
    # load the pdf file
    uploaded_pdf = genai.upload_file(pdf)
    response = model.generate_content(["Given the following pdf, I need you to extract the text. The text is from a book, and I only want the text that is relevant to the story (don't include the title, author, afternotes, things like that). Don't include any system responses; just provide me with the text from the story. Make sure you go through the entire pdf. ", uploaded_pdf])
    return response.text


def make_summary(text):
    response = model.generate_content("Given the following story, I need you to generate a summary of the story. I need the 6 most important parts of the story that contain the most action. If character names are present, do not include in the summary. I want a description of the scene that anyone could understand. Just provide me the 6 parts, each on a new line; don't use bullet points. There should be 6 lines total. Don't give system responses or give titles to the sections. Make sure to not give away the end of the story. The story is as follows: " + text)
    return response.text

def make_script(summary):

    script = model.generate_content("Given the following summary, I need you to generate 2 sentences for each part of the summary. The sentences should be purely descriptive and not contain any character names. It should have subject (any person, place, or thing, decsribe what the character is wearing, hairstyle, i.e. A handsome male model, A commercial airplane, two eggs), action (what the subject is doing, adjectives work well here, i.e. walking angrily, dancing happily), setting/mood (the location, include emotional ideas about the overall mood, i.e. a dusty motel, a busy city street, stormy clouds), shot (wide angle, close up, long shot, FPV, snorricam), style (reinforce the mood, i.e. Cinematic film, 80's Action Movie, add color grading ideas) for each part of the summary. Do not include any system responses in your response, and provide a new line between each part. These parts should not be connected to each other. They should be able to be interpreted on their own without needing context from other parts. The summary is as follows: " + summary)
    return script.text

@app.route('/api/extract_text', methods=['POST'])
def api_extract_text():
    pdf = request.files.get('pdf')
    if not pdf:
        return jsonify({"error": "No PDF file provided"}), 400

    # Save the uploaded PDF to a temporary location
    pdf_path = os.path.join("data", pdf.filename)
    pdf.save(pdf_path)

    # Extract text from the PDF
    extracted_text = extract_text(pdf_path)
    return jsonify({"text": extracted_text})

# Flask route to generate summary
@app.route('/api/make_summary', methods=['POST'])
def api_make_summary():
    data = request.get_json()
    text = data.get("text")
    if not text:
        return jsonify({"error": "No text provided"}), 400

    summary = make_summary(text)
    return jsonify({"summary": summary})

# Flask route to generate script
@app.route('/api/make_script', methods=['POST'])
def api_make_script():
    data = request.get_json()
    summary = data.get("summary")
    if not summary:
        return jsonify({"error": "No summary provided"}), 400

    script = make_script(summary)
    return jsonify({"script": script})

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)


'''
if __name__ == "__main__":

    base_path = "/Users/frankchang/Desktop/code/aiatl"
    file_path = os.path.join(base_path, "data/text.txt")


    text = extract_text(file_path)
    with open(os.path.join(base_path, "data/text.txt"), "w") as file:
        file.write(text)

    print("Text extracted and saved to data/text.txt")

    with open(file_path, "r") as file:
        text = file.read()

    # generate the summary
    summary = make_summary(text)

    # write the summary to the summary.txt file in /data/summary.txt
    with open(os.path.join(base_path, "data/summary.txt"), "w") as file:
        file.write(summary)

    print("Summary generated and saved to data/summary.txt")

    summary = os.path.join(base_path, "data/summary.txt")
    with open(summary, "r") as file:
        summary = file.read()
    # generate the script
    script = make_script(summary)

    # write the script to the script.txt file in /data/script.txt
    with open(os.path.join(base_path, "data/script3.txt"), "w") as file:
        file.write(script)
'''


