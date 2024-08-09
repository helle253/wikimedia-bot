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
  format = img.format
  fb = io.BytesIO()

  if (img.height > 4096 and img.height > img.width):
    resize_on_height(img).save(fb, format=format)
    return fb.getvalue()
  elif (img.width > 4096):
    resize_on_width(img).save(fb, format=format)
    return fb.getvalue()
  else:
    # do nothing
    return image_data
