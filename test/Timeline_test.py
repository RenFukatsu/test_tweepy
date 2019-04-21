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

reserve_id = []

public_tweets = api.home_timeline() # get timeline
for tweet in public_tweets:
    print(tweet.id) # show text of timeline
    reserve_id.append(tweet.id)


print("since")
public_tweets = api.home_timeline(since_id= reserve_id[10])
for tweet in public_tweets:
    print(tweet.id) # show text of timeline
    reserve_id.append(tweet.id)

print("max")
public_tweets = api.home_timeline(max_id= reserve_id[10])
for tweet in public_tweets:
    print(tweet.id) # show text of timeline
    reserve_id.append(tweet.id)

print("reserve")
print(reserve_id)
