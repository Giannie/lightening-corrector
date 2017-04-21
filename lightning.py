'''
LighteningCorrector
By Giancarlo Grasso
lightning.py
Copyright (c) 2017 Giancarlo Grasso (MIT License)
'''

import praw
from time import sleep
import time
import datetime
import re
import requests
import json
import spellcheck_config

ENDPOINT = "https://api.cognitive.microsoft.com/bing/v5.0/spellcheck/?"
HEADERS = {"Ocp-Apim-Subscription-Key": spellcheck_config.KEY}

text = '''Are you sure you didn't mean lightning? If you are talking about electrostatic discharge or Apple's connector, you mean "lightning".

lightning:

noun:

1. the occurrence of a natural electrical discharge of very short duration and high voltage between a cloud and the ground or within a cloud, accompanied by a bright flash and typically also thunder.
"A tremendous flash of lightning"

adjective:

1. very quick.
"A lightning cure for his hangover"

lighten:

verb:

1. to make lighter in weight.
"I am lightening the load on my truck"

2. to become lighter or less dark; brighten.
"The sky is lightening now that the storm has passed"

P.S. I'm only a bot, but I'm trying to learn. I can now actually check to see if you've misused the word "lightening" using spell checking APIs. If I have replied to you, it is now likely that you have made a mistake. Please reply if you think I'm wrong!
'''

def foundWord(comment):
    string = comment.body
    if re.search(r"\b" + re.escape("lightening") + r"\b", string.lower()):
        print("Checking", comment, "for misuse.")
        sentences = [sentence.strip() for sentence in re.split('[?!.]',string) if "lightening" in sentence.lower()]
        for sentence in sentences:
            url = ENDPOINT + "text=" + sentence + "&mode=proof"
            resp = requests.get(url, headers=HEADERS)
            if resp.ok:
                if "lightening" in [correction['token'] for correction in json.loads(resp.text)['flaggedTokens']]:
                    return True
        print("This one is fine")
    return False

reddit = praw.Reddit('lightning')
starting = True
while starting:
    try:
        username = reddit.user.me().name
        starting = False
    except:
        print("Could not connect to reddit, trying again")
        sleep(10)
comment_queue = []
then = 0
print("Starting to trawl comments")
for comment in reddit.subreddit('all').stream.comments():
    if username not in [str(comment.author), str(comment.parent().author)] and foundWord(comment):
        print("Adding comment",comment,"to queue")
        comment_queue.append(comment)
    if time.time() - then > 60:
        try:
            for c in comment_queue:
                age = datetime.datetime.utcnow() - datetime.datetime.utcfromtimestamp(c.created_utc)
                if age.seconds < 3600:
                    c.reply(text)
                    comment_queue.remove(c)
                    print("Replied to",comment,"removing from queue")
                    then = time.time() - 40
                else:
                    print(comment,"is too old, removing from queue")
                    comment_queue.remove(c)
        except praw.exceptions.APIException as error:
            then = time.time()
            print("Couldn't comment")
            print(error)
            sleep(1)
