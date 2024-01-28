import praw
import setup
import logging
import config
import util
import languageconfig as lang
from datetime import datetime
from util import log, debug
from modactions import remove_post
from config import REDDIT_USERNAME, TARGET_SUBREDDIT

# FrugalModBot reddit bot for /r/frugal
# Author: /u/mcagent

def main():
    # Configure the logging module
    logging.basicConfig(level = logging.INFO, filename = 'FrugalModBot.log')
    # Access PRAW API and sign into Reddit account
    reddit = setup.login()
    # The subreddit the bot is acting upon
    subreddit = reddit.subreddit(TARGET_SUBREDDIT)
    log(f'Found target subreddit /r/{subreddit.display_name}.')

    if not util.user_is_subreddit_mod(subreddit):
        log(f"/u/{REDDIT_USERNAME} is not a moderator of {TARGET_SUBREDDIT}. Exiting program.", is_error=True)
        exit(1)

    BOT_STARTUP_TIME = datetime.now()
    log(f'Bot started up at {BOT_STARTUP_TIME.strftime("%Y-%m-%d %H:%M:%S")}')

    # https://praw.readthedocs.io/en/stable/code_overview/other/subredditstream.html
    # Yields new Submissions as they become available. Submissions are yielded oldest first.
    for post in subreddit.stream.submissions():
        # The banned_by attribute is set when a post is removed.
        if post.banned_by != None:
            debug(f'{post.id} - Ignoreg due to banned_by attribute set to TRUE')
            continue

        # Don't do anything if a mod has approved the post.    
        if post.approved:
            debug(f'{post.id} - Ignoring due to SELF POST APPROVED')
            continue

        # Ignore old posts. This can be done with a submissions(skip_existing=True) argument,
        # however this does not allow us to check age of post in our later check.
        if util.post_age_in_minutes(post.created_utc) > 7200: # 5 days
            debug(f'{post.id} - Ignoring due to POST OLDER THAN 5 DAYS')
            continue

        if util.is_image_post(post):
            monitor_image_post(post)
        else:
            debug(f'{post.id} - Ignoring due to POST NOT OF TYPE IMAGE/DOES NOT CONTAIN IMAGE.')

def monitor_image_post(post: praw.models.Submission) -> None:
    debug(f'Entering monitor_image_posts() function for post {post.id}.')

    # We only want to check posts that aren't brand new to give the OP time to leave a comment or edit the post.
    if not util.post_is_sufficiently_old(post):
        debug(f'{post.id} - Post is not sufficiently old. Leaving monitor_image_posts().')
        return
    # Post title is sufficiently large.
    if len(post.title) >= config.POST_TITLE_CHARACTER_MINIMUM:
        debug(f'{post.id} - Post title is >= 150. Leaving monitor_image_posts().')
        return
    # If it's a self post and they included a long enough post body, do nothing
    if post.is_self and len(post.body) >= config.POST_CHARACTER_MINIMUM:
        debug(f'{post.id} - Post is self post and body is > char minimum. Leaving monitor_image_posts().')
        return
    
    # Find the largest (in character count) top-level comment from the author. May return nothing.    
    author_comment = util.author_biggest_comment(post)
    title_size = len(post.title)
    
    # Remove the post if there's no comment of sufficient size and a short title. Otherwise, report the post.
    if author_comment is None:
        if title_size < config.TITLE_LENGTH_REMOVAL or (post.is_self and len(post.body) < 100):
            remove_post(post, lang.FOLLOW_UP_OR_POORLY_DESCRIPTIVE_POST_REASON(post))
        elif title_size < config.POST_TITLE_CHARACTER_MINIMUM or ((post.is_self and len(post.body) < 150)):
            debug(f'Reported post {post.id} for insufficient title or body length.')
            post.report(lang.SHORT_POST_REPORT_REASON)
    else:
        comment_size = len(author_comment.body)

        if comment_size < config.COMMENT_LENGTH_REMOVAL:
            remove_post(post, lang.FOLLOW_UP_OR_POORLY_DESCRIPTIVE_POST_REASON(post))
        elif comment_size < config.COMMENT_CHARACTER_MINIMUM:
            debug(f'Reported post {post.id} for insufficient title or body length.')
            author_comment.report(lang.SHORT_COMMENT_REPORT_REASON)

if __name__ == "__main__":
    main()