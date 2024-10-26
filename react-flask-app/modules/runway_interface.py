from flask import Flask, request, jsonify
from runwayml import AsyncRunwayML
from dotenv import dotenv_values
import asyncio
from gemini_interface import generate_initial_image

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

async def main():
     # Define paths for the script and image save directory
    script_path = "react-flask-app/data/scripts/text.txt"
    image_save_dir = "react-flask-app/data/imgs"
    
    # Step 1: Generate an image using the first line from the script file
    image_path = generate_initial_image(script_path)

    # Step 2: Read the first line as the prompt text
    with open(script_path, "r") as file:
        prompt_text = file.readline().strip()   

    video_id = await generate_initial_video(prompt_text, image_path)
    print(f"Initial video generated with ID: {video_id}")        
