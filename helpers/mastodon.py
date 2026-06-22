from boto3 import client
from mastodon import Mastodon

from helpers.images import fit_image_to_constraint, to_bytes

ssm = client("ssm")
mastodon_access_key = ssm.get_parameter(Name="/wikimedia_bot/mastodon/access_key")[
    "Parameter"
]["Value"]
mastodon_api_base_url = ssm.get_parameter(Name="/wikimedia_bot/mastodon/base_url")[
    "Parameter"
]["Value"]

#   Set up Mastodon
mastodon = Mastodon(
    access_token=mastodon_access_key,
    api_base_url=mastodon_api_base_url,
)


def post(image, alt_text: str) -> None:
    try:
        resized_image = fit_image_to_constraint(image, 4096)
        media_id = mastodon.media_post(
            to_bytes(resized_image), "image", description=alt_text
        )["id"]
        mastodon.status_post("", media_ids=[media_id])
    except Exception as e:
        print("Error posting to Mastodon")
        print(e)
