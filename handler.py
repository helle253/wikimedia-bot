from helpers import bluesky, mastodon, twitter
from helpers.dynamodb import DynamoDBWrapper
from helpers.wikimedia import get_random_image

dynamodb = DynamoDBWrapper()


def post(file: dict[str, any]) -> None:
    bluesky.post(file)
    mastodon.post(file)
    twitter.post(file)


def handler(_, __):
    file = get_random_image()
    dynamodb.record_post_to_table(file["pageid"], file["title"])
    post(file)
