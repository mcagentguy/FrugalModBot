import praw
from util import log

from config import CLIENT_ID, USER_AGENT, REDDIT_USERNAME
from credentials import CLIENT_SECRET, REDDIT_PASSWORD

def login():
    try:
        reddit = praw.Reddit(client_id = CLIENT_ID, 
                     client_secret = CLIENT_SECRET,
                     user_agent = USER_AGENT,
                     username = REDDIT_USERNAME,
                     password = REDDIT_PASSWORD)
            
        log(f'Successfully signed in to /u/{REDDIT_USERNAME}.')
    # except praw.exceptions.OAuthException:
    #     util.log('Incorrect reddit username or password! Change this in the credentials.py file.')
    #     exit(1)
    except Exception as anError:
        log(str(anError), is_error=True)
        exit(1)

    return reddit
