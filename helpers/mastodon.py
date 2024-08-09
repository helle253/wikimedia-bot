from helpers.images import fit_image_to_constraint, get_image, to_bytes
from mastodon import Mastodon
from boto3 import client

ssm = client('ssm')
mastodon_access_key = ssm.get_parameter(Name='/wikimedia_bot/mastodon/access_key')['Parameter']['Value']
mastodon_api_base_url = ssm.get_parameter(Name='/wikimedia_bot/mastodon/base_url')['Parameter']['Value']

#   Set up Mastodon
mastodon = Mastodon(
  access_token = mastodon_access_key,
  api_base_url = mastodon_api_base_url,
)

def post(url: str) -> None:
  image = get_image(url)
  resized_image  = fit_image_to_constraint(image, 4096)
  image_bytes = to_bytes(resized_image)
  media_id = mastodon.media_post(image_bytes, 'image')['id']
  mastodon.status_post('', media_ids=[media_id])
