from mastodon import Mastodon
import requests
import os
from typing import Dict
import random

mastodon_access_key = os.getenv("MASTODON_ACCESS_KEY")
mastodon_api_base_url = os.getenv("MASTODON_BASE_URL")

#   Set up Mastodon
mastodon = Mastodon(
  access_token = mastodon_access_key,
  api_base_url = mastodon_api_base_url,
)

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
      ### TODO: Verify results have not already been posted.
      results = result['query']['categorymembers']
      ## randint is inclusive, so subtract 1 from length to prevent overflow errors
      range = len(results) - 1
      return results[random.randint(0, range)]
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

file = find_file_details()
url = get_file_url(file['title'])
image_data  = get_image_data(url)
print(url)
post(image_data)
