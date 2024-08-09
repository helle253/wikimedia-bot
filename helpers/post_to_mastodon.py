from helpers.fit_image_to_4096_px import fit_image_to_4096_px
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

def post_to_mastodon(image: bytes) -> None:
  resized_image  = fit_image_to_4096_px(image)
  media_id = mastodon.media_post(resized_image, 'image')['id']
  mastodon.status_post('', media_ids=[media_id])
