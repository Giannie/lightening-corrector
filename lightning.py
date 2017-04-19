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

P.S. I'm only a bot; I reply to anyone that uses the word "lightening", even if they used it correctly. I apologise if you have used this word correctly. If this is a skincare or makeup subreddit you should probably just ban me now. You guys definitely use lightening correctly more often than not.
'''

def foundWord(string):
    match = False
    substring = "lightening"
    false_matches = ["lightening up", "lightening the load"]
    result = re.search(r"\b" + re.escape(substring) + r"\b", string)
    while result:
        for f in false_matches:
            if string[result.start():].find(f) == 0:
                string = string[result.end():]
                result = re.search(r"\b" + re.escape(substring) + r"\b", string)
                break
        else:
            return True
    return False

reddit = praw.Reddit('lightning')
username = reddit.user.me().name
comment_queue = []
then = 0
print("Starting to trawl comments")
for comment in reddit.subreddit('all').stream.comments():
    if username != str(comment.author) and foundWord(comment.body.lower()):
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
