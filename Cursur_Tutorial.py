'''

Test tweepy by python3.6.7

Description: Show 30 tweets (only text) of follow people.

'''

import tweepy

# Each Twitter app gets its own CK and CS.
CK = 'IVPxRYYGz7zV4Nkbhh7n7W5e7' # API key / consumer_secret
CS = 'zHPj97mDBOnym3xxnmjYN5iJ10ia0m3HH26rXSqWE9U3bzAlY4' # API secret key / consumer_secret

# Each Twitter account has its own AT and AS.
AT = '1117047463112609792-LKTGrWWXY6agxYiGXdrhRT1x91J0KK' # Access token
AS = 'jF9MvoXWjHdhFu6KtdpiWfwrFiV1CbgjX8SHmvTR1Kk3J' # Access token secret

auth = tweepy.OAuthHandler(CK, CS) # App registration
auth.set_access_token(AT, AS) # Account registration

api = tweepy.API(auth) # creat a class of tweepy

# Iterate through all of the authenticated user's friends
for friend in tweepy.Cursor(api.friends).items(1):
    # Process the friend here
    print(friend._json)
