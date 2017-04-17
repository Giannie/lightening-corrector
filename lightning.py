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

text = '''Are you sure you didn't mean lightning? If you are talking about Apple's connector, you mean "lightning".

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

P.S. I'm only a bot; I reply to anyone that uses the word "lightening", even if they used it correctly. I apologise if you have used this word correctly.
'''

reddit = praw.Reddit('lightning')
comment_queue = []
then = 0
for comment in reddit.subreddit('all').stream.comments():
    if str(comment.author) != "lightningvlightening" and comment.body.lower().find("lightening") > -1:
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