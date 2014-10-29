'''
Created on 26 Oct 2014

@author: Jack The Ripper
'''

from slistener import SListener
import time, tweepy, sys
import json

consumer_key='qpUR91PwjvChszV0VFgrc4Hje'
consumer_secret='q9mPUZE2OsFbaqKUF32ZsY1ry4anZ1k8pNSne56wc3HInmERFu'
access_token='2845943577-R0g6YRlrdEqSFb2mKy5HXuByQPdpq4TLGrPkmSs'
access_token_secret='ed5emUSxHENLtqN8nLYvGkbipKAEemFd0fgjsXNPC8GED'
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)
def main():
    track = ['halloween']
 
    listen = SListener(api, '414-tweets')
    stream = tweepy.Stream(auth, listen)

    print "Streaming started..."

    try: 
        stream.filter(track = track)
    except:
        print "error!"
        stream.disconnect()

if __name__ == '__main__':
    main()
# public_tweets = api.home_timeline()
# user= tweepy.api.get_user('maddy93')
# l = StdOutListener()
# stream = tweepy.Stream(auth, l)
# stream.filter(track=['programming'])
# for tweet in public_tweets:
#     print tweet.text