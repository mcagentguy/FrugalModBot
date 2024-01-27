import praw
from util import log

from config import CLIENT_ID, USER_AGENT, REDDIT_USERNAME

try:
    from credentials import CLIENT_SECRET, REDDIT_PASSWORD
except ImportError:
    log("NOTICE: The 'credentials.py' file is missing.", is_error=True)
    log("Please create the 'credentials.py' file with the required variables CLIENT_SECRET and REDDIT_PASSWORD.", is_error=True)
    exit(1)

def login() -> None:
    try:
        reddit = praw.Reddit(client_id = CLIENT_ID, 
                     client_secret = CLIENT_SECRET,
                     user_agent = USER_AGENT,
                     username = REDDIT_USERNAME,
                     password = REDDIT_PASSWORD)
            
        log(f'Successfully signed in to /u/{REDDIT_USERNAME}.')
    except Exception as anError:
        log(str(anError), is_error=True)
        exit(1)

    return reddit
