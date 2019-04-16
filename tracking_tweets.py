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
    for tweet in public_tweets:
        if tweet.retweet_count > 100:
            temp = []
            try:
                temp = [tweet.retweeted_status.id, tweet.retweet_count]
                print("\nThis is retweets.\nuser : ",
                      tweet.retweeted_status.user.name,
                      "\ntext : \n",
                      tweet.retweeted_status.text,
                      "\nretweet : ",
                      tweet.retweet_count)
            except:
                temp = [tweet.id, tweet.retweet_count]
                print("\nuser : ",
                      tweet.user.name,
                      "\ntext : \n",
                      tweet.text,
                      "\nretweet : ",
                      tweet.retweet_count)

            temp2.append(temp)

    if temp2:
        for push in temp2[::-1]:
            tweet_id_retweets.append(push)


def manage_retweet():
    for id_retweets in tweet_id_retweets:
        tweet = api.get_status(id_retweets[0])
        if tweet.retweet_count - id_retweets[1] > 1:
            print("\nuser : ",
                  tweet.user.name,
                  "\ntext : \n",
                  tweet.text,
                  "\nretweet : ",
                  tweet.retweet_count)
        else:
            if not id_retweets == tweet_id_retweets:
                print("\ndelete the tweet")
                print(tweet.text)
                tweet_id_retweets.remove(id_retweets)


if __name__ == "__main__":
    show_retweet()

    while True:
        time.sleep(900)
        manage_retweet()
        time.slppe(10)
        show_retweet()

