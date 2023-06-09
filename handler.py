from mastodon import Mastodon
import requests
from typing import Dict, Union
from boto3 import client
from random import randrange
from datetime import timedelta, datetime

from helpers.dynamodb import DynamoDBWrapper
from helpers.fit_image_to_4096_px import fit_image_to_4096_px

ssm = client('ssm')
mastodon_access_key = ssm.get_parameter(Name='/wikimedia_bot/mastodon/access_key')['Parameter']['Value']
mastodon_api_base_url = ssm.get_parameter(Name='/wikimedia_bot/mastodon/base_url')['Parameter']['Value']

#   Set up Mastodon
mastodon = Mastodon(
  access_token = mastodon_access_key,
  api_base_url = mastodon_api_base_url,
)

dynamodb = DynamoDBWrapper()

def make_request(req):
  result = requests.get('https://commons.wikimedia.org/w/api.php', params=req).json()
  if 'error' in result:
    raise Exception(result['error'])
  if 'warnings' in result:
    print(result['warnings'])
  if 'query' in result:
    return result
  else:
    raise Exception('Something went wrong!')

def find_non_posted_image(results) -> Union[None, any]:
  '''
    Returns nothing if all the results have already been posted. 
    Otherwise, returns the id and title of an image that has not been posted.
  '''
  for result in results:
    print(result)
    if dynamodb.is_already_posted(result['pageid']):
      next
    else:
      return result

def random_time(
    start=datetime(2011,3,8,13),
    end=(datetime.now() - timedelta(weeks=4))
):
  delta = end - start
  int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
  random_second = randrange(int_delta)
  return start + timedelta(seconds=random_second)

##
# Returns a title and an ID, which can be used to query for the image itself.
def get_random_image_details() -> Dict[str, int]:
  request = {
    'action': 'query',
    'format': 'json',
    'list': 'categorymembers',
    'cmtype': 'file',
    'cmtitle': 'Category:Quality_images',
    'cmstart': random_time(),
    'cmsort': 'timestamp',
    'cmdir': 'ascending',
  };
  lastContinue = {}
  while (True):
    # Clone original request
    req = request.copy()
    # Modify it with the values returned in the 'continue' section of the last result.
    req.update(lastContinue)
    # Call API
    result = make_request(req)
    if 'query' in result:
      results = result['query']['categorymembers']
      fresh_result = find_non_posted_image(results)
      if fresh_result:
        return fresh_result
    lastContinue = result['continue']


def get_file_url(file_title: str) -> str:
  request = {
    'action': 'query',
    'format': 'json',
    'titles': [file_title],
    'prop': 'imageinfo',
    'iiprop': 'url',
  };
  result = requests.get('https://commons.wikimedia.org/w/api.php', params=request).json()
  return list(result['query']['pages'].values())[0]['imageinfo'][0]['url']

def get_image_data(url: str) -> bytes:
  headers = {'User-Agent': 'Wikimedia Bot' }
  resp = requests.get(url, headers=headers)
  if resp.status_code != 200:
      raise Exception('Something went wrong downloading the file!')
  return resp.content;

def post(file_data: bytes) -> None:
  media_id = mastodon.media_post(file_data, 'image')['id']
  mastodon.status_post('', media_ids=[media_id])

def handler(_, __):
  file = get_random_image_details()
  url = get_file_url(file['title'])
  image_data  = fit_image_to_4096_px(get_image_data(url))
  dynamodb.record_post_to_table(file['pageid'], file['title'])
  post(image_data)

if __name__ == "__main__":
    handler()
