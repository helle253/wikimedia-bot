import re
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

def post(file: Dict[str, any]) -> None:
  try:
    details = get_file_details(file['title'])
    image = get_image(details['url'])
    alt_text = details['extmetadata']['ImageDescription']['value']
    alt_text = re.sub('<[^<]+?>', '', alt_text)
    resized_image  = fit_image_to_constraint(image, 4096)
    media_id = mastodon.media_post(to_bytes(resized_image), 'image', description=alt_text)['id']
    mastodon.status_post('', media_ids=[media_id])
  except Exception as e:
    print('Error posting to Mastodon')
    print(e)
