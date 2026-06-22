import re

from helpers import bluesky, mastodon, twitter
from helpers.dynamodb import DynamoDBWrapper
from helpers.images import get_image
from helpers.wikimedia import get_file_details, get_random_image

dynamodb = DynamoDBWrapper()


def post(image, alt_text: str) -> None:
    bluesky.post(image, alt_text)
    mastodon.post(image, alt_text)
    twitter.post(image, alt_text)


def handler(_, __):
    file = get_random_image()
    details = get_file_details(file["title"])
    image = get_image(details["url"])
    alt_text = details["extmetadata"]["ImageDescription"]["value"]
    alt_text = re.sub("<[^<]+?>", "", alt_text)

    dynamodb.record_post_to_table(file["pageid"], file["title"])
    post(image, alt_text)
