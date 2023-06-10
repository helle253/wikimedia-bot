from PIL import Image
import io
import math

def fit_image_to_4096_px(image_data: bytes) -> bytes:
  img = Image.frombytes(image_data)

  if (img.height > 4096 and img.height > img.width):
    return resize_on_height(img)
  elif (img.width > 4096):
    return resize_on_width(img)
  else:
    # do nothing
    return image_data

def resize_on_height(img: Image):
  ratio = 4096 / img.height
  new_width = math.floor(img.width * ratio)
  img.resize((new_width, 4096))
  img_byte_arr = io.BytesIO()
  img.save(img_byte_arr, format=img.format)

  return img_byte_arr.getvalue()

def resize_on_width(img: Image):
  ratio = 4096 / img.width
  new_height = math.floor(img.height * ratio)
  img.resize((4096, new_height))
  img_byte_arr = io.BytesIO()
  img.save(img_byte_arr, format=img.format)

  return img_byte_arr.getvalue()

