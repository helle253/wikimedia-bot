from helpers.fit_image_to_4096_px import fit_image_to_4096_px
from mastodon import Mastodon

def post_to_mastodon(image: bytes) -> None:
  resized_image  = fit_image_to_4096_px(image)
  media_id = mastodon.media_post(resized_image, 'image')['id']
  mastodon.status_post('', media_ids=[media_id])
