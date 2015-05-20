#!/usr/bin/python

import sys
import random
import re
import twitter

_USERNAME = u'@DailyICD10'

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
    keywords = []
    text = status.text.replace(_USERNAME, "")
    print(text)

def getLastMentionId():
    #TODO
    return None

if __name__ == "__main__":
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

    sys.exit(0)
