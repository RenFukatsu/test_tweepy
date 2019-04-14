'''

Test tweepy by python3.6.7

Description: Show 20 tweets (only text) of follow people.

'''

import tweepy

# Each Twitter app gets its own CK and CS.
CK = '' # API key / consumer_key
CS = '' # API secret key / consumer_secret

# Each Twitter account has its own AT and AS.
AT = '' # Access token
AS = '' # Access token secret

# ----------------------------------------------------------------
# This part is to conceal my key. So you do not write this part.
import PathModule
CK = PathModule.consumer_key
CS = PathModule.consumer_secret_key
AT = PathModule.access_token
AS = PathModule.access_token_secret
# ----------------------------------------------------------------

auth = tweepy.OAuthHandler(CK, CS) # App registration
auth.set_access_token(AT, AS) # Account registration

api = tweepy.API(auth) # creat a class of tweepy

# Iterate through all of the authenticated user's friends
for friend in tweepy.Cursor(api.friends).items():
    # Process the friend here
    print(friend.status.text,"\nretweets : ",friend.status.retweet_count)
