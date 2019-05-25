'''

python3.6.7

Author : Ren Fukatsu

'''

import tweepy
import json
import sys
import PathModule
import time
import threading
import socket

CK = PathModule.consumer_key
CS = PathModule.consumer_secret_key
AT = PathModule.access_token
AS = PathModule.access_token_secret

auth = tweepy.OAuthHandler(CK, CS)
auth.set_access_token(AT, AS)

api = tweepy.API(auth_handler=auth)

cycle = 5 # minutes

lock = threading.Lock()


class ModelTweet():
    def __init__(self, tweet_id=0, user_name="", screen_name="",text="", media_type="", media_url={}, retweet_count=[], retweet_change=0, called_count=0):
        self.id = tweet_id
        self.user_name = user_name
        self.screen_name = screen_name
        self.url = "https://twitter.com/" + self.screen_name + "/status/" + str(self.id)
        self.text = text
        self.media_type = media_type
        self.media_url = media_url
        self.retweet_count = []
        self.retweet_count.extend(retweet_count)
        self.retweet_change = retweet_change
        self.called_count = called_count

class RetweetsManager():
    def __init__(self, ip, port):
        self.reserveTweets = []
        self.id_list = []
        self.address = ( ip, port)
        thread = threading.Thread(target=self.socket_server)
        thread.start()
        self.Run()

    def Run(self):
        while True:
            time_start = time.time()
            while time.time() - time_start < cycle * 60:
                if not self.GetSearch():
                    break
                self.RemoveSameRetweets(False)
                time.sleep(5)
    
            self.ConfirmRetweetsChange()
            self.SwapRetweetChangeRanking()
            #self.ConvertJson()
            self.ShowTweets()

    def GetSearch(self):
        try:
            search_tweets = api.search("RT", lang="ja", count=100) # 180/15min
        except: # limited
            print("limited api.search")
            return False

        for tweet in search_tweets:
            try:
                tweet = tweet.retweeted_status
            except:
                pass

            if tweet.retweet_count < 1000:
                continue
            
            media_url = {}
            media_type = ""
            try: # video
                for i in range(len(tweet.extended_entities["media"][0]["video_info"]["variants"])):
                    media_url[i] = tweet.extended_entities["media"][0]["video_info"]["variants"][i]["url"]
                    media_type = "video"
            except:
                try: # photo
                    for i in range(len(tweet.extended_entities["media"])):
                        media_url[i] = tweet.extended_entities["media"][i]["media_url"]
                    media_type = "photo"
                except: # text
                    media_type = "text"
            
            self.reserveTweets.append(ModelTweet(tweet_id=tweet.id, user_name=tweet.user.name, screen_name=tweet.user.screen_name, text=tweet.text, media_type=media_type, media_url=media_url, retweet_count=[tweet.retweet_count]))
            self.id_list.append(tweet.id)
        
        return True
        
    def RemoveSameRetweets(self, flag):
        self.reserveTweets.sort(reverse=True, key=lambda tweet:(tweet.id, tweet.retweet_count[0]))

        before_tweet = self.reserveTweets[-1]
        removeTweets = []

        for tweet in self.reserveTweets:
            if tweet.id == before_tweet.id:
                if tweet.user_name == "":
                    removeTweets.append(tweet)
                else:
                    removeTweets.append(before_tweet)
                tweet.called_count += 1 + before_tweet.called_count
                if flag:
                    tweet.retweet_count.extend(before_tweet.retweet_count)
                    if len(tweet.retweet_count) > (60//cycle + 1):
                        del tweet.retweet_count[0]
                    if tweet.retweet_count[-1] - tweet.retweet_count[0] > 1000 or len(tweet.retweet_count) < (60//cycle + 1):
                        tweet.retweet_change = tweet.retweet_count[-1] - tweet.retweet_count[0]
                    else:
                        removeTweets.append(tweet)
            before_tweet = tweet
        
        for tweet in removeTweets:
            try:
                self.reserveTweets.remove(tweet)
            except:
                print(tweet.id)
                pass

        if flag:
            return

        self.id_list.sort()

        before_id = 0
        removeId = []

        for tweet_id in self.id_list:
            if tweet_id == before_id:
                removeId.append(tweet_id)
            before_id = tweet_id
        
        for tweet_id in removeId:
            try:
                self.id_list.remove(tweet_id)
            except:
                pass

    def SpilitList(self, n):
        for idx in range(0, len(self.id_list), n):
            yield self.id_list[idx:idx+n]


    def ConfirmRetweetsChange(self):
        split_id_list = list(self.SpilitList(100))
        for i in range(len(split_id_list)):
            try:
                nowStatus = api.statuses_lookup(split_id_list[i])
            except:
                print("limit api.status_lookup")
                return

            for tweet in nowStatus:
                self.reserveTweets.append(ModelTweet(tweet_id=tweet.id, retweet_count=[tweet.retweet_count]))

        self.RemoveSameRetweets(True)
    
    def SwapRetweetChangeRanking(self):
        self.reserveTweets.sort(reverse=True, key=lambda tweet:tweet.retweet_change)
    
    def ConvertJson(self):
        dictJson = {}

        for i in range(len(self.reserveTweets)):
            if i > 100:
                break
            dict_retweet_count = {}
            for j in range(len(self.reserveTweets[i].retweet_count)):
                dict_retweet_count[j] = self.reserveTweets[i].retweet_count[j]
            
            dictJson[i] = {
                "id" : self.reserveTweets[i].id,
                "url" : self.reserveTweets[i].url,
                "user_name" : self.reserveTweets[i].user_name,
                "screen_name" : self.reserveTweets[i].screen_name,
                "text" : self.reserveTweets[i].text,
                "media" : {
                    "type" : self.reserveTweets[i].media_type,
                    "url" : self.reserveTweets[i].media_url
                },
                "retweet_count" : dict_retweet_count,
                "retweet_count_change" : self.reserveTweets[i].retweet_change,
                "called_count" : self.reserveTweets[i].called_count
            }

        strJson = json.dumps(dictJson, ensure_ascii=False)

        return strJson
    
    def socket_server(self):
        global lock
        sock = socket.socket()
        sock.bind(self.address)
        sock.listen(1)
        while True:
            conn, address = sock.accept()
            data = conn.recv(1024)
            if not data:
                break
            lock.acquire()
            strJson = data.decode('utf-8')
            dictJson = json.loads(strJson)

            if(dictJson["command"] == "get_all_data"):
                self.SwapRetweetChangeRanking()
                sendMsg = self.ConvertJson()
                sendByte = sendMsg.encode('utf-8')

                conn.sendall(sendByte)
            else:
                sendData = {
                    "seq" : dictJson["seq"],
                    "command" : dictJson["command"],
                    "data" : None
                }
                sendMsg = json.dumps(sendData, ensure_ascii=False)
                sendByte = sendMsg.encode('utf-8')

                conn.sendall(sendByte)
            
            lock.release()
            conn.close()
        
        sock.close()
    
    def ShowTweets(self):
        print("---------------------Ranking----------------------")
        for tweet in self.reserveTweets:
            if tweet.retweet_change > 1000:
                print("change : ", tweet.retweet_change, "\tid : ", tweet.id, "\tretweet : ", tweet.retweet_count[-1])
    

def main():
    retweetsManager = RetweetsManager("127.0.0.1", 5008)

if __name__ == "__main__":
    main()
