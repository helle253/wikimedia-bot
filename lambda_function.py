from mastodon import Mastodon
import requests
import os
from typing import Dict, Union

from aws_helpers.dynamodb import DynamoDBWrapper

mastodon_access_key = os.getenv('MASTODON_ACCESS_KEY')
mastodon_api_base_url = os.getenv('MASTODON_BASE_URL')

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


##
# Returns a title and an ID, which can be used to query for the image itself.
def find_file_details() -> Dict[str, int]:
  request = {
    'action': 'query',
    'format': 'json',
    'list': 'categorymembers',
    'cmtype': 'file',
    'cmtitle': 'Category:Quality_images',
    'cmlimit': 'max',
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

def lambda_handler(_, __):
  file = find_file_details()
  url = get_file_url(file['title'])
  image_data  = get_image_data(url)
  dynamodb.record_post_to_table(file['pageid'], file['title'])
  post(image_data)
