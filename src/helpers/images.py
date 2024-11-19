import io
from PIL import Image
import math

import requests

def _resize_on_height(img: Image, max_height: int) -> Image:
  ratio = max_height / img.height
  new_width = math.floor(img.width * ratio)

  return img.resize((new_width, max_height))

def _resize_on_width(img: Image, max_width: int) -> Image:
  ratio = max_width / img.width
  new_height = math.floor(img.height * ratio)

  return img.resize((max_width, new_height))

def fit_image_to_constraint(image: Image, constraint=4096) -> Image:
  if (image.height > constraint and image.height > image.width):
    return _resize_on_height(image, constraint)
  elif (image.width > constraint):
    return _resize_on_width(image, constraint)
  else:
    # do nothing
    return image

def get_image(url: str) -> Image:
  headers = {'User-Agent': 'Wikimedia Bot' }
  resp = requests.get(url, headers=headers)

  print(f'downloading {url}')

  if resp.status_code != 200:
      raise Exception('Something went wrong downloading the file!')
  return Image.open(io.BytesIO(resp.content))

def to_bytes(image: Image) -> bytes:
  format = image.format or 'JPEG'
  image_data = io.BytesIO()
  print(format)
  image.save(image_data, format=format)
  return image_data.getvalue()
