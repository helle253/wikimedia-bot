import tweepy
from boto3 import client
from typing import Dict

from helpers.images import fit_image_to_constraint, get_image, to_bytes
from helpers.wikimedia import get_file_details

ssm = client('ssm')
consumer_key = ssm.get_parameter(Name='/wikimedia_bot/twitter/api_key')['Parameter']['Value']
consumer_secret = ssm.get_parameter(Name='/wikimedia_bot/twitter/api_key_secret')['Parameter']['Value']
access_token = ssm.get_parameter(Name='/wikimedia_bot/twitter/access_token')['Parameter']['Value']
access_token_secret = ssm.get_parameter(Name='/wikimedia_bot/twitter/access_token_secret')['Parameter']['Value']

auth = tweepy.OAuth1UserHandler(consumer_key, consumer_secret, access_token, access_token_secret)
api = tweepy.API(auth)
client = tweepy.Client(consumer_key=consumer_key, consumer_secret=consumer_secret,
                       access_token=access_token, access_token_secret=access_token_secret)

def post(file: Dict[str, any]) -> None:
  details = get_file_details(file['title'])
  description_url = details['descriptionurl']
  image = get_image(details['url'])
  resized_image  = fit_image_to_constraint(image, 2048)
  media_upload = api.simple_upload(f'image.{image.format}', file=to_bytes(resized_image))
  api.create_media_metadata(media_upload.media_id, alt_text=description_url)
  client.create_tweet(media_ids=[media_upload.media_id])
