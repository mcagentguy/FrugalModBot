import praw
import setup
import logging
import config
import util
import languageconfig as lang
from datetime import datetime
from util import log
from modactions import remove_post
from config import REDDIT_USERNAME, TARGET_SUBREDDIT

def main():
    # Configure the logging module
    logging.basicConfig(level = logging.INFO, filename = 'FrugalModBot.log')
    # Access PRAW API and sign into Reddit account
    reddit = setup.login()
    # The reddit user account object for the bot
    user = reddit.redditor(REDDIT_USERNAME)
    # The subreddit the bot is acting upon
    subreddit = reddit.subreddit(TARGET_SUBREDDIT)
    log(f'Found target subreddit /r/{subreddit.display_name}.')

    if not util.user_is_subreddit_mod(user, subreddit):
        log(f"/u/{REDDIT_USERNAME} is not a moderator of {TARGET_SUBREDDIT}. Exiting program.", is_error=True)
        exit(1)

    BOT_STARTUP_TIME = datetime.now()
    log(f'Bot started up at {BOT_STARTUP_TIME.strftime("%Y-%m-%d %H:%M:%S")}')

    """
    All logged in and setup. begin monitoring for new posts.
    """

    # Grab startup stream. This is what keeps the program looping.
    # https://praw.readthedocs.io/en/stable/code_overview/other/subredditstream.html

    # SubredditStream
    # Yields new Submissions as they become available. Submissions are yielded oldest first.
    for post in subreddit.stream.submissions():
        post_timestamp = datetime.utcfromtimestamp(post.created_utc)

        # Ignore old posts. This can be done with a submissions(skip_existing=True) argument,
        # however this does not allow us to check age of post in our later check.
        if post_timestamp < BOT_STARTUP_TIME:
            continue

        if util.is_image_post(post):
            monitor_image_posts(post)

def monitor_image_posts(post):
    # We only want to check posts that aren't brand new to give the OP time to leave a comment or edit the post.
    if util.post_is_sufficiently_old(post):
        return

    # If it's a self post and they included a long enough post body, do nothing
    if post.is_self and len(post.body) >= config.POST_CHARACTER_MINIMUM:
        return

    # Find the largest (in character count) top-level comment from the author. May return nothing.    
    author_comment = util.author_biggest_comment(post)

    if author_comment is None:
        remove_post(post, lang.FOLLOW_UP_OR_POORLY_DESCRIPTIVE_POST_REASON(post))
    elif len(author_comment.body) < 150:
        author_comment.report(lang.SHORT_COMMENT_REPORT_REASON)

if __name__ == "__main__":
    main()