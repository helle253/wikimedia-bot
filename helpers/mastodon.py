from typing import Dict
from helpers.images import fit_image_to_constraint, get_image, to_bytes
from mastodon import Mastodon
from boto3 import client

from helpers.wikimedia import get_file_details

ssm = client('ssm')
mastodon_access_key = ssm.get_parameter(Name='/wikimedia_bot/mastodon/access_key')['Parameter']['Value']
mastodon_api_base_url = ssm.get_parameter(Name='/wikimedia_bot/mastodon/base_url')['Parameter']['Value']

#   Set up Mastodon
mastodon = Mastodon(
  access_token = mastodon_access_key,
  api_base_url = mastodon_api_base_url,
)

def build_message(details: Dict[str, any]) -> str:
    artist_url = details['extmetadata']['Artist']['value']
    creation_time = details['extmetadata']['DateTimeOriginal']['value']
    return f"<a href=\"{details['descriptionurl']}\">{creation_time}</a> by {artist_url}"

def post(file: Dict[str, any]) -> None:
  try:
    details = get_file_details(file['title'])
    image = get_image(details['url'])
    alt_text = details['extmetadata']['ImageDescription']['value']
    resized_image  = fit_image_to_constraint(image, 4096)
    media_id = mastodon.media_post(to_bytes(resized_image), 'image', description=alt_text)['id']
    text = build_message(details)
    mastodon.status_post(text, media_ids=[media_id])
  except Exception as e:
    print('Error posting to Mastodon')
    print(e)
