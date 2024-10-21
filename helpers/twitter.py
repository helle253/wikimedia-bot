import tweepy
from boto3 import client

ssm = client('ssm')
consumer_key = ssm.get_parameter(Name='/wikimedia_bot/twitter/api_key')['Parameter']['Value']
consumer_secret = ssm.get_parameter(Name='/wikimedia_bot/twitter/api_key_secret')['Parameter']['Value']
access_token = ssm.get_parameter(Name='/wikimedia_bot/twitter/access_token')['Parameter']['Value']
access_token_secret = ssm.get_parameter(Name='/wikimedia_bot/twitter/access_token_secret')['Parameter']['Value']

client = tweepy.Client(consumer_key=consumer_key, consumer_secret=consumer_secret,
                       access_token=access_token, access_token_secret=access_token_secret)

def post(url: str) -> None:
  client.create_tweet('Hello World!')
