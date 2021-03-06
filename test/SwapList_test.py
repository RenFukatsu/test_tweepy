'''

Test tweepy by python3.6.7

Description: 

'''

import tweepy
import time

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

api = tweepy.API(auth_handler=auth) # creat a class of tweepy

tweet_id_retweets = []

def show_retweet():
    try:
        public_tweets = api.home_timeline(since_id=tweet_id_retweets[-1][0])
    except:
        public_tweets = api.home_timeline()

    temp2 = []
    print("show")
    for tweet in public_tweets:
        temp = []
        try:
            temp = [tweet.id, tweet.retweeted_status.id, tweet.retweet_count, 0]
        except:
            temp = [tweet.id, tweet.id, tweet.retweet_count, 0]

        temp2.append(temp)
        print(tweet.id)

    print("temp")
    if temp2:
        for push in temp2[::-1]:
            print(push[0])
            tweet_id_retweets.append(push)



if __name__ == "__main__":
    show_retweet()
    show_retweet()

