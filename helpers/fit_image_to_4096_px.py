from PIL import Image
import io
import math

def resize_on_height(img: Image) -> Image:
  ratio = 4096 / img.height
  new_width = math.floor(img.width * ratio)

  return img.resize((new_width, 4096))

def resize_on_width(img: Image) -> Image:
  ratio = 4096 / img.width
  new_height = math.floor(img.height * ratio)

  return img.resize((4096, new_height))

def fit_image_to_4096_px(image_data: bytes) -> bytes:
  img = Image.open(io.BytesIO(image_data))

  if (img.height > 4096 and img.height > img.width):
    return resize_on_height(img).tobytes()
  elif (img.width > 4096):
    return resize_on_width(img).tobytes()
  else:
    # do nothing
    return image_data
