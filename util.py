import time
import logging
import config
import datetime as dt
from datetime import datetime

def log(aStringToLog, is_error=False):
    if is_error:
        print('ERROR: ' + aStringToLog)
        logging.error(time.strftime("%Y/%m/%d %H:%M:%S ") + aStringToLog)
    else:
        print(aStringToLog)
        logging.info(time.strftime("%Y/%m/%d %H:%M:%S ") + aStringToLog)

def user_is_subreddit_mod(reddit_user, subreddit):
    return subreddit.name in [subreddit.name.lower() for aSub in reddit_user.moderated()]

# This check can normally be done by checking the value of the post_hint attribute.
 # Many subreddits however, including /r/Frugal, do not share this information.
 # The workaround in this function is to check whether it's a self post, and if it is,
# check for image extensions: .png, .jpg, .jpeg, .gif and etc.
def is_image_post(post):
    if not post.is_self:
        return True  # Non-self posts are considered image posts by default

    body = post.selftext.lower()

    return any(extension in body for extension in config.IMAGE_EXTENSIONS)

# post.comments.list() returns top level comments
def author_biggest_comment(post):
    max_length = 0
    max_length_comment = None

    for comment in post.comments.list():
        if comment.author == post.author:
            comment_length = len(comment.body)
            if comment_length > max_length:
                max_length = comment_length
                max_length_comment = comment

    return max_length_comment

def post_is_sufficiently_old(post):
    current_time = datetime.now(dt.timezone.utc)
    time_posted = datetime.utcfromtimestamp(post.created_utc).replace(tzinfo=dt.timezone.utc)

    return (current_time - time_posted).total_seconds() >= config.POST_AGE_BEFORE_BOT_CHECKS_COMMENTS