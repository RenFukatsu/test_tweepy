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

reserve_tweets = []
count = 0

class ReserveRetweeets:
    def __init__(self, tweet_id, user_name, tweet_text, media_url, retweet_count, retweet_count_change):
        self.tweet_id = tweet_id
        self.user_name =user_name
        self.tweet_text =tweet_text
        self.media_url = media_url
        self.retweet_count = []
        self.retweet_count.append(retweet_count)
        self.retweet_count_change = retweet_count_change

class RetweetsManager():
    global reserve_tweets
    def GetSearch(self):
        public_tweets = api.search("RT",lang="ja", count=100) # 180/15min

        for tweet in public_tweets:
            if tweet.retweet_count > 1000:
                media_url = []
                try:
                    for i in range(len(tweet.extended_entities["media"][0]["video_info"]["variants"])):
                        media_url.append(tweet.extended_entities["media"][0]["video_info"]["variants"][i]["url"])
                except:
                    try:
                        for i in range(len(tweet.extended_entities["media"])):
                            media_url.append(tweet.extended_entities["media"][i]["media_url"])
                    except:
                        pass

                try:
                    temp_tweet = ReserveRetweeets(tweet.retweeted_status.id, tweet.retweeted_status.user.name, tweet.retweeted_status.text, media_url, tweet.retweeted_status.retweet_count, 0)
                except:
                    temp_tweet = ReserveRetweeets(tweet.id, tweet.user.name, tweet.text, media_url, tweet.retweet_count, 0)
                reserve_tweets.append(temp_tweet)

    def RemoveSameRetweets(self):
        reserve_tweets.sort(reverse=True,key=lambda x:(x.tweet_id, x.retweet_count[0]))
        temp_tweets = 0
        temp_tweet_id = 0
        temp_remove_tweets = []
        for tweets in reserve_tweets:
            if tweets.tweet_id == temp_tweet_id:
                temp_remove_tweets.append(temp_tweets)
            
            temp_tweets = tweets
            temp_tweet_id = tweets.tweet_id
        
        for tweets in temp_remove_tweets:
            reserve_tweets.remove(tweets)

    def ComfirmRetweetsChange(self):
        temp_remove_tweets = []
        for tweets in reserve_tweets:
            try:
                tweet = api.get_status(tweets.tweet_id) # 180/15min
                tweets.retweet_count.append(tweet.retweet_count)
            except:
                print("limit")
                pass
            if len(tweets.retweet_count) > 60:
                del tweets.retweet_count[0]
            if tweets.retweet_count[-1] - tweets.retweet_count[0] > 1000 or len(tweets.retweet_count) != 60:
                tweets.retweet_count_change = tweets.retweet_count[-1] - tweets.retweet_count[0]
            else:
                temp_remove_tweets.append(tweets)
        
        for tweets in temp_remove_tweets:
            reserve_tweets.remove(tweets)
    
    def ShowAllRetweets(self):
        print("-------------Ranking-----------------")
        for tweets in reserve_tweets:
            print("Retweets:", tweets.retweet_count[-1], "\t", "id:", tweets.tweet_id, "\t", "change:", tweets.retweet_count_change)
            #print("\nRetweet : ",
            #      tweets.retweet_count
            #      "\nUser : ",
            #      tweets.user_name,
            #      "\nText : \n",
            #      tweets.tweet_text,)

    def SwapRetweetRanking(self):
        reserve_tweets.sort(reverse=True,key=lambda x:x.retweet_count_change)
    
def p():
    global count
    print(count)
    count += 1


def main():
    retweetsManager = RetweetsManager()

    while True:
        for i in range(60):
            try:
                retweetsManager.GetSearch()
            except:
                pass
            retweetsManager.RemoveSameRetweets()
            time.sleep(5)
        retweetsManager.ComfirmRetweetsChange()
        retweetsManager.SwapRetweetRanking()
        retweetsManager.ShowAllRetweets()

if __name__ == "__main__":
    main()
