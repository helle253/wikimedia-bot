from helpers import mastodon, twitter
from helpers.dynamodb import DynamoDBWrapper
from helpers.wikimedia import get_random_image

dynamodb = DynamoDBWrapper()


def post(file: dict[str, any]) -> None:
    mastodon.post(file)
    twitter.post(file)


def handler(_, __):
    file = get_random_image()
    dynamodb.record_post_to_table(file["pageid"], file["title"])
    post(file)
