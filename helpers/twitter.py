import tweepy
from boto3 import client
from PIL import Image
import io
import random

from helpers.image_resizing import fit_image_to_file_size

ssm = client('ssm')
bearer_token = ssm.get_parameter(Name='/wikimedia_bot/twitter/bearer_token')['Parameter']['Value']

auth = tweepy.OAuth2BearerHandler(bearer_token)

api = tweepy.API(auth)
client = tweepy.Client(bearer_token)

de#f post(image: bytes) -> None:
  #resized_image = fit_image_to_file_size(image)
  #image_file = io.BytesIO(resized_image)
  #filename = f'/tmp/image-{random.randint(0, 1000000)}.{Image.open(image_file).format.lower()}'
  #with open(filename, 'wb') as f:
  #  f.write(resized_image)
  #media = api.media_upload(filename, media=image_file)
  #media_id = media.id
  #client.create_tweet(media_ids=[media_id])

