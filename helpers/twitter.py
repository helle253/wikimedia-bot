import tweepy
from boto3 import client

ssm = client('ssm')
bearer_token = ssm.get_parameter(Name='/wikimedia_bot/twitter/bearer_token')['Parameter']['Value']

auth = tweepy.OAuth2BearerHandler(bearer_token)

api = tweepy.API(auth)
client = tweepy.Client(bearer_token)

def post(url: str) -> None:
  print('Tweeted!')
