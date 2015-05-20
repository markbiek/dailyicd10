#!/usr/bin/python

import sys
import random
import re
import twitter

_USERNAME = u'@DailyICD10'
_LINES = []

def loadAccessToken():
    vals = {}
    tokenFile = 'access.token'

    if len(sys.argv) > 1:
        tokenFile = sys.argv[1]

    for line in open(tokenFile):
        (key, val) = line.strip().split('=')
        vals[key] = val

    return vals

def mentionToString(status):
    print("------------")
    print(status.user.name, status.user.id)
    print(status.text)
    print(status.id)

def isDirectMention(status):
    global _USERNAME

    return status.text[0:len(_USERNAME)] == _USERNAME

def getMentions():
    since_id = getLastMentionId()
    all_mentions = api.GetMentions(since_id=since_id)
    mentions = []

    for status in all_mentions:
        if isDirectMention(status):
            #mentionToString(status)

            mentions.append(status)

    return mentions

def getStatusKeywords(status):
    keywords = status.text.replace(_USERNAME, "").split(',')

    return keywords

def getDescriptionFromKeyword(keyword):
    global _LINES

    results = [desc for desc in _LINES if keyword in desc]

    if len(results) <= 0:
        return ""
    else:
        return random.choice(results)

def getLastMentionId():
    #TODO
    return None

if __name__ == "__main__":
    _LINES = open('/home/mark/dev/icd-10/icd10.txt').readlines()

    tokens = loadAccessToken()
    if ("key" not in tokens.keys() or 
            "secret" not in tokens.keys() or 
            "consumer_key" not in tokens.keys() or 
            "consumer_secret" not in tokens.keys()):
        print "ERROR: Invalid access token file."
        sys.exit(1)

    api = twitter.Api(consumer_key=tokens['consumer_key'],
                        consumer_secret=tokens['consumer_secret'],
                        access_token_key=tokens['key'],
                        access_token_secret=tokens['secret'])

    mentions = getMentions()

    for status in mentions:
        keywords = getStatusKeywords(status)

        for keyword in keywords:
            desc = getDescriptionFromKeyword(keyword)

            if desc == "":
                desc = "Sorry, couldn't find anything for " + keyword

            reply = "@" + status.user.screen_name + " " + desc

            try:
                ret = api.PostUpdate(reply)
                if ret is None:
                    print "WARNING: PostUpdate returned None. Your post may have failed."
            except:
                #TODO
                pass

    sys.exit(0)
