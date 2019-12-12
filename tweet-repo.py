# Databricks notebook source
import re
import tweepy
import requests
from tweepy import OAuthHandler
from textblob import TextBlob
from azure.servicebus.control_client import ServiceBusService
import demjson
from time import sleep
import datetime
import json
import http.client, urllib.request,urllib.parse, urllib.error, base64,json

class TwitterClient(object):
  def __init__(self):
      # keys and tokens from the Twitter Dev Console
      consumer_key = "LdtDHkDbbQL1wopKfvIp0nSGQ"
      consumer_secret = "YKVIePK7YTWba7bpVhaGJHLxiB57Mqdeo8k2nyN7x0k59bvGLG"
      access_token = "1130364337128820736-kdFGQHTORxgUOEIgLWK67RbkGBGGW5"
      access_token_secret = "FsSW4SZ2R8sJMggo0Rk3Lj1hxeSukfYIwYnU4b7cPYtlh"

      # attempt authentication
      try:
          # create OAuthHandler object
          self.auth = OAuthHandler(consumer_key, consumer_secret)
          # set access token and secret
          self.auth.set_access_token(access_token, access_token_secret)
          # create tweepy API object to fetch tweets
          self.api = tweepy.API(self.auth)
      except:
          print("Error: Authentication Failed")

  def clean_tweet(self, tweet):
      return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) |(\w+:\/\/\S+)", " ", tweet).split())

  def get_tweet_sentiment(self, tweet):
      # create TextBlob object of passed tweet text
      analysis = TextBlob(self.clean_tweet(tweet))
      # set sentiment
      if analysis.sentiment.polarity > 0:
          return 'positive'
      elif analysis.sentiment.polarity == 0:
          return 'neutral'
      else:
          return 'negative'

#   def get_tweets(self, query, count = 10):
#       # empty list to store parsed tweets
#       tweets = []

#       try:
#           # call twitter api to fetch tweets
#           fetch
#           # set access token and secret
#           self.auth.set_access_token(access_token, access_token_secret)
#           # create tweepy API object to fetch tweets
#           self.api = tweepy.API(self.auth)
#       except:
#           print("Error: Authentication Failed")

  def clean_tweet(self, tweet):
      return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) |(\w+:\/\/\S+)", " ", tweet).split())

  def get_tweet_sentiment(self, tweet):
      # create TextBlob object of passed tweet text
      analysis = TextBlob(self.clean_tweet(tweet))
      # set sentiment
      if analysis.sentiment.polarity > 0:
          return 'positive'
      elif analysis.sentiment.polarity == 0:
          return 'neutral'
      else:
          return 'negative'

  def get_tweets(self, query, count):
      # empty list to store parsed tweets
      tweets = []

      try:
          # call twitter api to fetch tweets
          fetched_tweets = self.api.search(q = query, count = count)

          # parsing tweets one by one
          for tweet in fetched_tweets:
              # empty dictionary to store required params of a tweet
              parsed_tweet = {}

              # saving text of tweet
              parsed_tweet['text'] = tweet.text
              entities = tweet.entities
              parsed_tweet['hashtags'] = entities
              retweet_count = tweet.retweet_count
              retweet_status =tweet.retweeted
              parsed_tweet['status'] = retweet_status
              parsed_tweet['retweet_count'] = retweet_count
#               parsed_tweet['hashtags'] = tweet.hashtags
              # saving sentiment of tweet
              parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text)

              # appending parsed tweet to tweets list
              if tweet.retweet_count > 0:
                  # if tweet has retweets, ensure that it is appended only once
                  if parsed_tweet not in tweets:
                      tweets.append(parsed_tweet)
              else:
                  tweets.append(parsed_tweet)

          # return parsed tweets
          return tweets

      except tweepy.TweepError as e:
          # print error (if any)
          print("Error : " + str(e))

def extracting_tweets():
  # creating object of TwitterClient Class
  api = TwitterClient()
  tweets = api.get_tweets(query = '#AxisBank OR #axisBank OR @axisbank OR #Axisbank OR @AxisBank' , count = 10)
  return tweets

def identify_tweets(tweet):
  lowercase_tweet = tweet.lower()
  if "icici" in lowercase_tweet:
    return "ICICI"
  elif "hdfc" in lowercase_tweet:
    return "HDFC"
  elif "axis" in lowercase_tweet:
    return "AXIS"
  elif "citibank" in lowercase_tweet:
    return "CitiBank"
  elif "kotakmahindra" in lowercase_tweet:
    return "Kotak Mahindra"
  elif "yesbank" in lowercase_tweet:
    return "Yes Bank"
  else:
    return "irrelevant"

def identify_hash(hashtag,tweet_sentiment):
  if hashtag == None:
    return "neutral"
  elif tweet_sentiment == "positive":
    return "positive"
  elif tweet_sentiment== "negative":
    return "negative"

def identify_sentiment(score):
  if score>0.5:
    return "positive"
  elif score<0.5:
    return "negative"
  elif score ==0.5:
    return "neutral"

counter = 0
number_of_tweets = 0
service_name = 'AtelierEventHub'
key_name = 'RootManageSharedAccessKey' # SharedAccessKeyName from Azure portal
key_value = 'ac0yntubZL9onKvZQDpWy06HwpcZmI5ivk5ykN3G37Y=' # SharedAccessKey from Azure portal
sbs = ServiceBusService(service_name,shared_access_key_name=key_name,shared_access_key_value=key_value)

while True:
  new_list = []
  recieved = extracting_tweets()
  sleep(3)
  number_of_tweets += 1
#   json = demjson.encode(data)
  for tweet in recieved:
    API_dict = {}
    API_dict = {"id":str(number_of_tweets), "text":tweet['text']}
    inner_dict =json.dumps(API_dict)
    final_api_dict_language = {"documents":[API_dict]}
    language_sending = json.dumps(final_api_dict_language)
    conn=http.client.HTTPSConnection("ateliersentitementanalysis.cognitiveservices.azure.com")
    headers =  {"Ocp-Apim-Subscription-Key":"c4066b974aca4126b3f7495bc6dec441","Content-Type":"application/json"}
    conn.request("POST","/text/analytics/v2.1/languages",language_sending,headers)
    response=conn.getresponse()
    data=response.read()
    response_in_string = data.decode("utf-8")
    language_dict = json.loads(response_in_string)
    print(language_dict)
    language_raw_dict = language_dict['documents']
    language_code = language_raw_dict[0]['detectedLanguages'][0]['iso6391Name']
    language_name = language_raw_dict[0]['detectedLanguages'][0]['name']
#     Sentiment API
    Sentiment_API_dict = {"id":str(number_of_tweets),"language":language_code, "text":tweet['text']}
    final_api_dict_language = {"documents":[Sentiment_API_dict]}
    sentiment_url = "https://ateliersentitementanalysis.cognitiveservices.azure.com/text/analytics/v2.1/sentiment"
    headers =  {"Ocp-Apim-Subscription-Key":"c4066b974aca4126b3f7495bc6dec441","Content-Type":"application/json"}
    response = requests.post(sentiment_url, headers=headers, json=final_api_dict_language)
    sentiment_result_string = response.content
    sentiment_result_string = sentiment_result_string.decode("utf-8")
    sentiment_result_dict =json.loads(sentiment_result_string)
    sentiment_score = sentiment_result_dict["documents"][0]['score']
    tweet_text = tweet['text']
    tweet_hash = tweet['hashtags']['hashtags']
    rt_status = tweet['status']
    rt_count = tweet['retweet_count']
    tweet_date = str(datetime.datetime.now())
    length_of_hash = len(tweet_hash)
    if (length_of_hash>0):
      hashtags = tweet_hash[0]['text']
    else:
      hashtags = None
    source = identify_tweets(tweet_text)
    sentiment_word = identify_sentiment(sentiment_score)
    hashtag_sentiment = identify_hash(hashtags,sentiment_word)
    
    sending_to_event_hub_json = {"tweet":tweet_text,"hashtags":hashtags,"retweet_status":rt_status,"retweet_count":rt_count,"tweet_date":tweet_date,"sentiment_score":sentiment_score,"language":language_name,"Company":source,"sentiment":sentiment_word,"hashtag_sentiment":hashtag_sentiment}
    json_to_event_hub = json.dumps(sending_to_event_hub_json)
    sbs.send_event("ateliereventhub",json_to_event_hub)
    print(json_to_event_hub)
    print("sent")
    print(counter)
    sleep(5)
    counter = counter +1
#   print("sending"+json)
  sleep(2)
#   print("sent"+str(counter))

# COMMAND ----------

