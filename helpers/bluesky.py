import re

from atproto import Client
from boto3 import client as boto_client

from helpers.images import (
    fit_image_to_constraint,
    fit_image_to_filesize,
    get_image,
    to_bytes,
)
from helpers.wikimedia import get_file_details

ssm = boto_client("ssm")
bluesky_handle = ssm.get_parameter(Name="/wikimedia_bot/bluesky/handle")["Parameter"][
    "Value"
]
bluesky_app_password = ssm.get_parameter(Name="/wikimedia_bot/bluesky/app_password")[
    "Parameter"
]["Value"]

bluesky_client = Client()
bluesky_client.login(bluesky_handle, bluesky_app_password)


def post(file: dict[str, any]) -> None:
    try:
        details = get_file_details(file["title"])
        image = get_image(details["url"])
        alt_text = details["extmetadata"]["ImageDescription"]["value"]
        alt_text = re.sub("<[^<]+?>", "", alt_text)

        resized_image = fit_image_to_constraint(image, 2000)
        resized_image = fit_image_to_filesize(resized_image, 1)

        upload_result = bluesky_client.upload_blob(to_bytes(resized_image))

        bluesky_client.send_post(
            text="",
            embed={
                "$type": "app.bsky.embed.images",
                "images": [{"alt": alt_text, "image": upload_result.blob}],
            },
        )
    except Exception as e:
        print("Error posting to Bluesky")
        print(e)
