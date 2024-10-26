from runwayml import AsyncRunwayML
from dotenv import dotenv_values
import asyncio

config = dotenv_values(".env")

# client = RunwayML(
#     api_key=config["RUNWAYML_API_SECRET"],
# )

client = AsyncRunwayML(
    api_key=config["RUNWAYML_API_SECRET"],
)

async def generate_video(prompt_text: str, ) -> str:
    image_to_video = await client.image_to_video.create(
        model="gen3a_turbo",
        prompt_text=prompt_text,
    )
    return image_to_video.id