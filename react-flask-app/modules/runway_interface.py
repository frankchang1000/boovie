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
async def generate_video(prompt_text: str, prompt_image_path: str) -> str:
    image_to_video = await client.image_to_video.create(
        model="gen3a_turbo",
        prompt_image = prompt_image_path,
        prompt_text=prompt_text
    )
    return image_to_video.id


# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
