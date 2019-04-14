'''

Test tweepy by python3.6.7

Description: counts retweets.

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

api = tweepy.API(auth_handler=auth) # creat a class of tweepy


if __name__ == "__main__":
    public_tweets = api.home_timeline()

    for tweet in public_tweets:
        try:
            print("\nThis is retweets.\nuser : ", 
                  tweet.retweeted_status.user.name, 
                  "\ntext : \n", 
                  tweet.retweeted_status.text, 
                  "\nretweet : ", 
                  tweet.retweet_count) 
        except:
            print("\nuser : ", 
                  tweet.user.name, 
                  "\ntext : \n", 
                  tweet.text, 
                  "\nretweet : ", 
                  tweet.retweet_count) 

