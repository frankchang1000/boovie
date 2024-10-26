from flask import Flask, request, jsonify
from runwayml import AsyncRunwayML
from dotenv import dotenv_values
import asyncio
import time

# Load environment configuration
config = dotenv_values(".env")

# Initialize the Async RunwayML client
client = AsyncRunwayML(api_key=config["RUNWAYML_API_SECRET"])

# Define asynchronous function to generate and extend video segments
async def generate_video_sequence(prompts, images):
    # Generate the initial 5-second video
    video_task = await client.image_to_video.create(
        model="gen3a_turbo",
        prompt_text=prompts[0],
        duration=5
    )
    video_id = video_task.id

    # Sequentially create new video segments for remaining prompts
    for i in range(1, len(prompts)):
        prompt = prompts[i]
        image_url = images[i] if i < len(images) else None  # Optional image for the segment

        # Generate a new segment to extend the video narrative
        video_task = await client.image_to_video.create(
            model="gen3a_turbo",
            prompt_text=prompt,
            prompt_image=image_url,
            duration=5
        )
        
        # Wait for task completion and update video_id for tracking
        video_id = video_task.id  # Update the video ID for the next segment
        time.sleep(1)  # Optional delay to avoid rate-limiting

    return video_id  # Return the ID of the last video segment generated

# Flask setup
app = Flask(__name__)

# Define the API endpoint to trigger the video generation
@app.route('/api/generate_video_sequence', methods=['POST'])
def api_generate_video_sequence():
    data = request.get_json()
    prompts = data.get("prompts")
    images = data.get("images", [None] * len(prompts))

    # Validate input
    if not prompts or not isinstance(prompts, list) or len(prompts) == 0:
        return jsonify({"error": "Prompts list is required and cannot be empty."}), 400

    # Run the async video sequence generation function in a synchronous context
    try:
        video_id = asyncio.run(generate_video_sequence(prompts, images))
        return jsonify({"final_video_id": video_id})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
