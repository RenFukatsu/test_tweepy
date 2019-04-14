'''

Test tweepy by python3.6.7

Description: Show 30 tweets (only text) of follow people.

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

# Iterate through all of the authenticated user's friends
for friend in tweepy.Cursor(api.friends).items(1):
    # Process the friend here
    print(friend._json)
