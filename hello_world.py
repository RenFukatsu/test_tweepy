'''

Test tweepy by python3.6.7

Description: Show 20 tweets (only text) of follow people.

'''

import tweepy

# Each Twitter app gets its own CK and CS.
CK = '' # API key / consumer_secret
CS = '' # API secret key / consumer_secret

# Each Twitter account has its own AT and AS.
AT = '' # Access token
AS = '' # Access token secret

auth = tweepy.OAuthHandler(CK, CS) # App registration
auth.set_access_token(AT, AS) # Account registration

api = tweepy.API(auth) # creat a class of tweepy

public_tweets = api.home_timeline() # get timeline
for tweet in public_tweets:
    print(tweet.text) # show text of timeline
