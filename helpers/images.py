import io
import math

import requests
from PIL import Image


def _resize_on_height(img: Image, max_height: int) -> Image:
    ratio = max_height / img.height
    new_width = math.floor(img.width * ratio)

    return img.resize((new_width, max_height))


def _resize_on_width(img: Image, max_width: int) -> Image:
    ratio = max_width / img.width
    new_height = math.floor(img.height * ratio)

    return img.resize((max_width, new_height))


def fit_image_to_constraint(image: Image, constraint=4096) -> Image:
    if image.height > constraint and image.height > image.width:
        return _resize_on_height(image, constraint)
    elif image.width > constraint:
        return _resize_on_width(image, constraint)
    else:
        # do nothing
        return image


def fit_image_to_filesize(
    image: Image, max_size_mb: float, quality_step: int = 2
) -> Image:
    """
    Resize image to fit within a maximum file size in MB.
    Uses iterative quality reduction and dimension scaling if needed.
    """
    format = image.format or "JPEG"

    current_image = image.copy()
    quality = 95

    while quality > 75:
        image_data = io.BytesIO()
        current_image.save(image_data, format=format, quality=quality)
        size_mb = len(image_data.getvalue()) / (1024 * 1024)

        if size_mb <= max_size_mb:
            return current_image

        quality -= quality_step

    scale_factor = 0.9
    for _ in range(20):
        new_width = math.floor(current_image.width * scale_factor)
        new_height = math.floor(current_image.height * scale_factor)

        if new_width < 400 or new_height < 400:
            return current_image

        current_image = image.resize((new_width, new_height))

        image_data = io.BytesIO()
        current_image.save(image_data, format=format, quality=85)
        size_mb = len(image_data.getvalue()) / (1024 * 1024)

        if size_mb <= max_size_mb:
            return current_image

        scale_factor -= 0.05

    return current_image


def get_image(url: str) -> Image:
    headers = {"User-Agent": "Wikimedia Bot"}
    resp = requests.get(url, headers=headers)

    print(f"downloading {url}")

    if resp.status_code != 200:
        raise Exception("Something went wrong downloading the file!")
    return Image.open(io.BytesIO(resp.content))


def to_bytes(image: Image) -> bytes:
    format = image.format or "JPEG"
    image_data = io.BytesIO()
    print(format)
    image.save(image_data, format=format)
    return image_data.getvalue()
