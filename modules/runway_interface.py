from flask import Flask, request, jsonify
from runwayml import AsyncRunwayML
from dotenv import dotenv_values
import asyncio

# Load environment configuration
config = dotenv_values(".env")

# Initialize the Async RunwayML client
client = AsyncRunwayML(
    api_key=config["RUNWAYML_API_SECRET"],
)

# Define asynchronous video generation function
async def generate_video(prompt_text: str) -> str:
    image_to_video = await client.image_to_video.create(
        model="gen3a_turbo",
        prompt_text=prompt_text,
    )
    return image_to_video.id

# Initialize Flask app
app = Flask(__name__)

# Define Flask route to trigger video generation
@app.route('/api/generate_video', methods=['POST'])
def api_generate_video():
    data = request.get_json()
    prompt_text = data.get("prompt_text")
    
    if not prompt_text:
        return jsonify({"error": "No prompt text provided"}), 400

    # Run the async function within Flask's synchronous request
    try:
        video_id = asyncio.run(generate_video(prompt_text))
        return jsonify({"video_id": video_id})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
