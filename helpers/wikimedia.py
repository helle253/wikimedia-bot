from datetime import datetime, timedelta
from random import randrange
from typing import Any

import requests

from helpers.dynamodb import DynamoDBWrapper

dynamodb = DynamoDBWrapper()


def _random_time(start=datetime(2011, 3, 8, 13), end=None) -> str:
    end = end or (datetime.now() - timedelta(weeks=4))
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = randrange(int_delta)
    random_datetime = start + timedelta(seconds=random_second)
    # Format as ISO 8601 timestamp for the Wikimedia API
    return random_datetime.strftime("%Y-%m-%dT%H:%M:%SZ")


def _make_request(req):
    headers = {
        "User-Agent": "WikimediaBot/1.0 "
        + "(https://github.com/helle253/wikimedia-bot; nathanhellbhoy@gmail.com) "
        + "python-requests"
    }
    result = requests.get(
        "https://commons.wikimedia.org/w/api.php", params=req, headers=headers
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
        "list": "categorymembers",
        "cmtype": "file",
        "cmtitle": "Category:Quality_images",
        "cmsort": "timestamp",
        "cmdir": "ascending",
    }
    while True:
        # Set a new random start time for each attempt
        request["cmstart"] = _random_time()
        lastContinue = {}

        # Paginate through results from this random start time
        while True:
            # Clone original request
            req = request.copy()
            # Modify it with the values returned in
            # the 'continue' section of the last result.
            req.update(lastContinue)
            # Call API
            result = _make_request(req)
            if "query" in result:
                results = result["query"]["categorymembers"]
                fresh_result = _find_non_posted_image(results)
                if fresh_result:
                    return fresh_result

            # If there's a continue token, keep paginating
            if "continue" in result:
                lastContinue = result["continue"]
            else:
                # No more pages from this random start time,
                # break to try a new random time
                break


def get_file_details(file_title: str) -> dict[str, any]:
    request = {
        "action": "query",
        "format": "json",
        "titles": [file_title],
        "prop": "imageinfo",
        "iiprop": "extmetadata|url",
    }
    headers = {
        "User-Agent": "WikimediaBot/1.0 "
        + "(https://github.com/helle253/wikimedia-bot; nathanhellbhoy@gmail.com) "
        + "python-requests"
    }
    result = requests.get(
        "https://commons.wikimedia.org/w/api.php", params=request, headers=headers
    ).json()
    result_list = list(result["query"]["pages"].values())
    print(result_list)
    return result_list[0]["imageinfo"][0]
