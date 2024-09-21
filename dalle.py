# Author : Massoud Ibrahim
# Date 2024-06-04
# dalle.py file has the functions required for /draw command.

from openai import OpenAI

client = OpenAI()

async def generate_image(prompt):
    response = client.images.generate(
    model="dall-e-3",
    prompt=prompt,
    n=1,
    size="1024x1024")
    return response.data[0].url
