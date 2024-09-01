import aiohttp
from PIL import Image
from io import BytesIO
import aiofiles

async def fetch_image(url: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                return await response.read()
            else:
                raise Exception(f"Failed to fetch image from {url}")

async def process_image(image_bytes: bytes):
    with Image.open(BytesIO(image_bytes)) as img:
        img = img.convert("RGB")
        img = img.resize((int(img.width / 2), int(img.height / 2)))
        output_bytes = BytesIO()
        img.save(output_bytes, format="JPEG")
        return output_bytes.getvalue()

async def save_image(file_path: str, image_bytes: bytes):
    async with aiofiles.open(file_path, 'wb') as f:
        await f.write(image_bytes)
