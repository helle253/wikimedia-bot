from typing import Any

import requests

from helpers.dynamodb import DynamoDBWrapper
from helpers.http import wikimedia_headers

dynamodb = DynamoDBWrapper()


def _make_request(req):
    result = requests.get(
        "https://commons.wikimedia.org/w/api.php",
        params=req,
        headers=wikimedia_headers(),
    ).json()
    if "error" in result:
        raise Exception(result["error"])
    if "warnings" in result:
        print(result["warnings"])
    if "query" in result:
        return result
    else:
        raise Exception("Something went wrong!")


def _find_non_posted_image(results) -> None | Any:
    """
    Returns nothing if all the results have already been posted.
    Otherwise, returns the id and title of an image that has not been posted.
    """
    for result in results:
        if not dynamodb.is_already_posted(result["pageid"]):
            return result
    return None


##
# Returns a title and an ID, which can be used to query for the image itself.
def get_random_image() -> dict[str, int]:
    request = {
        "action": "query",
        "format": "json",
        "list": "search",
        "srsearch": 'incategory:"Quality images"',
        "srnamespace": "6",  # File namespace
        "srsort": "random",
        "srlimit": "max",
    }
    while True:
        result = _make_request(request)
        results = result["query"]["search"]

        for result in results:
            if not dynamodb.is_already_posted(result["pageid"]):
                return {
                    "pageid": result["pageid"],
                    "title": result["title"],
                }


def get_file_details(file_title: str) -> dict[str, any]:
    request = {
        "action": "query",
        "format": "json",
        "titles": [file_title],
        "prop": "imageinfo",
        "iiprop": "extmetadata|url",
    }
    result = requests.get(
        "https://commons.wikimedia.org/w/api.php",
        params=request,
        headers=wikimedia_headers(),
    ).json()
    result_list = list(result["query"]["pages"].values())
    print(result_list)
    return result_list[0]["imageinfo"][0]
