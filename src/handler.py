
from typing import Dict

from helpers import mastodon, twitter, bluesky
from helpers.dynamodb import DynamoDBWrapper
from helpers.wikimedia import get_random_image

dynamodb = DynamoDBWrapper()

def post(file: Dict[str, any]) -> None:
  mastodon.post(file)
  twitter.post(file)
  bluesky.post(file)

def handler(_, __):
  file = get_random_image()
  dynamodb.record_post_to_table(file['pageid'], file['title'])
  post(file)
