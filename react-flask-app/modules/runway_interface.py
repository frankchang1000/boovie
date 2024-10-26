from flask import Flask, request, jsonify
from runwayml import AsyncRunwayML
from dotenv import dotenv_values
import asyncio
from gemini_interface import generate_initial_image

# Load environment configuration
config = dotenv_values(".env")

# Initialize the Async RunwayML client
client = AsyncRunwayML(api_key=config["RUNWAYML_API_SECRET"])

# Initialize Flask app
app = Flask(__name__)

# Define asynchronous video generation function
async def generate_video(prompt_text: str, prompt_image_path: str) -> str:
    image_to_video = await client.image_to_video.create(
        model="gen3a_turbo",
        prompt_image=prompt_image_path,
        prompt_text=prompt_text,
        duration=5  # Specify the duration of each video segment
    )
    return image_to_video.id

# Function to generate videos from prompts and images
async def generate_videos(script_path: str, image_save_dir: str):
    video_ids = []

    # Step 1: Generate an image using the first line from the script file
    image_path = generate_initial_image(script_path)

    # Step 2: Read all lines from the script as prompts
    with open(script_path, "r") as file:
        prompts = [line.strip() for line in file.readlines()]

    # Step 3: Generate the initial video
    initial_prompt = prompts[0]
    initial_video_id = await generate_video(initial_prompt, image_path)
    video_ids.append(initial_video_id)

    # Step 4: Generate videos for the remaining prompts and images
    for i in range(1, len(prompts)):
        prompt_text = prompts[i]
        image_path = generate_initial_image(script_path)  # Generate a new image for each prompt

        # Generate video segment and add to list
        video_id = await generate_video(prompt_text, image_path)
        video_ids.append(video_id)

    return video_ids

# Flask route to trigger video generation
@app.route('/api/generate_videos', methods=['POST'])
def api_generate_videos():
    # Define paths for the script and image save directory
    script_path = "react-flask-app/data/scripts/text.txt"
    image_save_dir = "react-flask-app/data/imgs"

    try:
        # Run the async function and gather video IDs
        video_ids = asyncio.run(generate_videos(script_path, image_save_dir))
        return jsonify({"video_ids": video_ids})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)

