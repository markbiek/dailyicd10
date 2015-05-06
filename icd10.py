#!/usr/bin/python

import sys
import random
import re
import twitter

def loadAccessToken():
    vals = {}
    tokenFile = 'access.token'

    if len(sys.argv) > 1:
        tokenFile = sys.argv[1]

    for line in open(tokenFile):
        (key, val) = line.strip().split('=')
        vals[key] = val

    return vals

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

    line = random.choice(open('icd10.txt').readlines())

    ret = api.PostUpdate(line)
    if ret is None:
        print "WARNING: PostUpdate returned None. Your post may have failed."
        sys.exit(2)

    sys.exit(0)
