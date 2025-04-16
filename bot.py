import discord
from datetime import datetime, date
from PIL import Image, ImageDraw, ImageFont
import io
import os
import asyncio

TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = int(os.getenv("GUILD_ID"))

intents = discord.Intents.default()
client = discord.Client(intents=intents)

def generate_image_with_number(number: str) -> io.BytesIO:
    size = 512
    img = Image.new('RGB', (size, size), color=(30, 30, 30))
    draw = ImageDraw.Draw(img)

    # Подгружаем нормальный шрифт
    font_path = "fonts/Roboto-Bold.ttf"
    try:
        font = ImageFont.truetype(font_path, 200)
    except:
        font = ImageFont.load_default()

    bbox = draw.textbbox((0, 0), number, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    text_x = (size - text_width) / 2
    text_y = (size - text_height) / 2 - bbox[1]  # Коррекция вертикального смещения

    draw.text(
        (text_x, text_y),
        number,
        font=font,
        fill=(255, 255, 255)
    )

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
    
    target_date = date(2026, 4, 17)
    today_date = date.today()
    days_left = (target_date - today_date).days
    
    img_bytes = generate_image_with_number(str(days_left))

    try:
        await guild.edit(icon=img_bytes.read())
        print("Avatar updated!")
    except Exception as e:
        print("Error updating avatar:", e)
    await client.close()

client.run(TOKEN)
