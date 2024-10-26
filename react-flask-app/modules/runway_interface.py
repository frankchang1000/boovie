
from runwayml import AsyncRunwayML
from dotenv import dotenv_values
import asyncio
from gemini_interface import generate_initial_image
from moviepy.editor import VideoFileClip, concatenate_videoclips

# Load environment configuration
config = dotenv_values(".env")

# Initialize the Async RunwayML client
client = AsyncRunwayML(api_key=config["RUNWAYML_API_SECRET"])


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

async def stitch_videos(video_ids: list, output_path: str):
    video_clips = []
    for video_id in video_ids:
        # Download the video asynchronously and add it to the list of clips
        video_path = await client.video.download(video_id)
        video_clip = VideoFileClip(video_path)
        video_clips.append(video_clip)

    # Concatenate the video clips into one final video
    final_clip = concatenate_videoclips(video_clips)
    final_clip.write_videofile(output_path, codec="libx264", fps=24)

    # Close all video clips to release resources
    for clip in video_clips:
        clip.close()

    return output_path