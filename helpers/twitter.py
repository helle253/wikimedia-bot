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

def build_message(details: Dict[str, any]) -> str:
    artist_url = details['extmetadata']['Artist']['value']
    creation_time = details['extmetadata']['DateTimeOriginal']['value']
    return f"{creation_time} by {artist_url} ({details['descriptionurl']})"

def post(file: Dict[str, any]) -> None:
  try:
    details = get_file_details(file['title'])
    alt_text = details['extmetadata']['ImageDescription']['value']
    image = get_image(details['url'])
    resized_image  = fit_image_to_constraint(image, 2048)
    media_upload = api.simple_upload(f'image.{image.format}', file=to_bytes(resized_image))
    api.create_media_metadata(media_upload.media_id, alt_text=alt_text)
    text = build_message(details)
    client.create_tweet(text=text, media_ids=[media_upload.media_id])
  except Exception as e:
    print('Error posting to Twitter')
    print(e)
