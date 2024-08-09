
from typing import Dict, Union

from helpers import mastodon, twitter
from helpers.dynamodb import DynamoDBWrapper
from helpers.wikimedia import get_file_urls, get_random_image_details

dynamodb = DynamoDBWrapper()

def post(file: Dict[str, any]) -> None:
  mastodon.post(file)
  twitter.post(file)

def handler(_, __):
  file = get_random_image_details()
  dynamodb.record_post_to_table(file['pageid'], file['title'])
  post(file)
