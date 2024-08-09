import requests
from typing import Dict, Union
from random import randrange
from datetime import timedelta, datetime

from helpers import dynamodb

dynamodb = dynamodb.DynamoDBWrapper()

def random_time(
    start=datetime(2011,3,8,13),
    end=(datetime.now() - timedelta(weeks=4))
):
  delta = end - start
  int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
  random_second = randrange(int_delta)
  return start + timedelta(seconds=random_second)

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
