#!/usr/bin/env python 

import requests
import json
import datetime
import csv
import time 

import gpiozero 
from time import sleep 


# if you haven't had an app_id, sign up one here: https://developers.facebook.com/apps

app_id = "1794678177523862"
app_secret = "34e6aa4a65d9cdfc427a115eae2cbccd" # DO NOT SHARE WITH ANYONE!

access_token = app_id + "|" + app_secret

#page which analysis is done
page_id = 'najibrazak'


#to catch error (such as "HTTP Error 500 (Internal Error)") and try again after a few seconds, which usually works and to consolidates the data retrival code
def request_until_succeed(url):
    req = requests.get(url)
    success = False
    while success is False:
        try:
            if req.status_code == 200: ## try to catch HTTP code 200 which means OK! 
                success = True
        except Exception:
            time.sleep(5)
            print ("Error for URL %s: %s" % (url, datetime.datetime.now()))

    return req.text


#to return the FB postfeeds by changing the page metadata endpoint to /feed endpoint
def getFacebookPageFeed(page_id, access_token):
    
    # construct the URL string
    base = "https://graph.facebook.com/v2.12"
    node = "/" + page_id + "/feed" 
    parameters = "/?access_token=%s" % access_token
    url = base + node + parameters
    
    # retrieve data
    data = json.loads(request_until_succeed(url))
    return data
    

#to return the FB a few postfeeds by changing the page metadata endpoint to /feed endpoint
def getFacebookPageFeedData(page_id, access_token, num_statuses):
    
    # construct the URL string
    base = "https://graph.facebook.com/v2.12"
    node = "/" + page_id + "/feed" 
    parameters = "/?fields=message,link,created_time,type,name,id,likes.limit(1).summary(true),comments.limit(1).summary(true),shares&limit=%s&access_token=%s" % (num_statuses, access_token) 
    url = base + node + parameters
    print(url)
    
    # retrieve data
    data = json.loads(request_until_succeed(url))
    return data
    

def getReactionsForStatuses(page_id, access_token, num_statuses):
    reactionData = {}
    reaction_types = ["like", "love", "wow", "haha", "sad", "angry"] 

    base = "https://graph.facebook.com/v2.12"
    node = "/" + page_id + "/feed" 
    for reaction in reaction_types: 
        reactionUpper = reaction.upper()
        reaction_type = "reactions_" + reaction 

        parameters = "/?fields=reactions.type(%s).limit(0).summary(total_count).as(%s)&limit=%s&access_token=%s" % (reactionUpper, reaction_type, num_statuses, access_token) 
        url = base + node + parameters

        # retrieve data
        data = json.loads(request_until_succeed(url))
        reactionData[reaction] = data["data"][0][reaction_type]["summary"]["total_count"]
    return reactionData

# test_status = getFacebookPageFeed(page_id, access_token)
# test_status = getFacebookPageFeedData(page_id, access_token, 1)["data"][0]["shares"]
test_status = getReactionsForStatuses(page_id, access_token, 1) 
print (test_status)
# print(json.dumps(test_status, indent=4, sort_keys=True))


