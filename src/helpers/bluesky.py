from atproto import Client
from typing import Dict
from helpers.images import get_image
from boto3 import client

from helpers.wikimedia import get_file_details

ssm = client('ssm')
bluseky_username = ssm.get_parameter(Name='/wikimedia_bot/bluesky/username')['Parameter']['Value']
bluesky_password = ssm.get_parameter(Name='/wikimedia_bot/bluesky/password')['Parameter']['Value']

#   Set up Bluesky client
client = Client()
client.login(bluseky_username, bluesky_password)

def post(file: Dict[str, any]) -> None:
  try:
    details = get_file_details(file['title'])
    image = get_image(details['url'])
    client.send_image(image)
  except Exception as e:
    print('Error posting to Bluesky')
    print(e)
