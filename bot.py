import discord
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
import io
import os
import asyncio

TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = int(os.getenv("GUILD_ID"))

intents = discord.Intents.default()
client = discord.Client(intents=intents)

def generate_image_with_number(number: str) -> io.BytesIO:
    img = Image.new('RGB', (256, 256), color=(30, 30, 30))
    draw = ImageDraw.Draw(img)
    font = ImageFont.load_default()
    text_width, text_height = draw.textsize(number, font=font)
    draw.text(((256 - text_width) / 2, (256 - text_height) / 2), number, font=font, fill=(255, 255, 255))

    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)
    return buffer

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")
    guild = client.get_guild(GUILD_ID)
    if guild is None:
        print("Guild not found")
        await client.close()
        return

    today = datetime.now().strftime("%d")
    img_bytes = generate_image_with_number(today)

    try:
        await guild.edit(icon=img_bytes.read())
        print("Avatar updated!")
    except Exception as e:
        print("Error updating avatar:", e)
    await client.close()

client.run(TOKEN)
