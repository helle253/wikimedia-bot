from PIL import Image
import io
import math

def _resize_on_height(img: Image, max_height: int) -> Image:
  ratio = max_height / img.height
  new_width = math.floor(img.width * ratio)

  return img.resize((new_width, max_height))

def _resize_on_width(img: Image, max_width: int) -> Image:
  ratio = max_width / img.width
  new_height = math.floor(img.height * ratio)

  return img.resize((max_width, new_height))

def fit_image_to_constraint(image_data: bytes, constraint=4096) -> bytes:
  img = Image.open(io.BytesIO(image_data))
  format = img.format
  fb = io.BytesIO()

  if (img.height > constraint and img.height > img.width):
    _resize_on_height(img, constraint).save(fb, format=format)
    return fb.getvalue()
  elif (img.width > constraint):
    _resize_on_width(img, constraint).save(fb, format=format)
    return fb.getvalue()
  else:
    # do nothing
    return image_data


def fit_image_to_file_size(image_data: bytes, max_file_size_mb=14) -> bytes:
  # Get the image size in bytes
  initial_size = len(image_data)
  initial_size_mb = initial_size / (1024 * 1024)

  if initial_size_mb <= max_file_size_mb:
      return image_data

  img = Image.open(io.BytesIO(image_data))

  # Calculate the new size ratio
  size_ratio = (max_file_size_mb / initial_size_mb) ** 0.5
  new_width = int(img.width * size_ratio)
  new_height = int(img.height * size_ratio)

  # Resize the image
  fb = io.BytesIO()
  img.resize((new_width, new_height)).save(fb, format=img.format)
  return fb.getvalue()

