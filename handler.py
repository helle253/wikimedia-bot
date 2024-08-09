
from typing import Union

from helpers import mastodon, twitter
from helpers.dynamodb import DynamoDBWrapper
from helpers.wikimedia import get_file_url, get_random_image_details

dynamodb = DynamoDBWrapper()

def post(url: str) -> None:
  mastodon.post(url)
  twitter.post(url)

def handler(_, __):
  file = get_random_image_details()
  url = get_file_url(file['title'])
  dynamodb.record_post_to_table(file['pageid'], file['title'])
  post(url)
