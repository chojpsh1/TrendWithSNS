import requests 
from requests_oauthlib import OAuth1
from influxDB_python import database
import datetime
import sys

consumer_key = ""
consumer_secret = ""
access_token = ""
access_token_secret = ""

oauth = OAuth1(client_key=consumer_key, client_secret=consumer_secret, resource_owner_key=access_token, resource_owner_secret=access_token_secret)

twit_id = sys.argv[1]
since_id = sys.argv[2]
def get_information():
    url = 'https://api.twitter.com/1.1/statuses/user_timeline.json?screen_name={0}'.format(twit_id)
    url += '&count=70&since_id='+since_id
    r = requests.get(url=url, auth=oauth)
    statuses = r.json()

    db = database()
    total_likes = 0
    for status in statuses:
        curl_insert = db.insert_query
        curl_insert += db.id_insert_query % (twit_id, status['id'], status['favorite_count'], status['retweet_count'], status['user']['followers_count'])
        curl_insert += "' >/dev/null 2>&1"
        #curl_insert += "'"
        total_likes += int(status['favorite_count'])
        db.insert(curl_insert)
    total_insert = db.insert_query
    total_insert += "likes,id="+twit_id+" total_likes="+str(total_likes)+"\n' >/dev/null 2>&1"
    db.insert(total_insert)

get_information()
