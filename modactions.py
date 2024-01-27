
import praw
from util import log
from config import REMOVE_POSTS

def report_post(post: praw.models.Submission, reason: str) -> None:
    post.report(reason)

def remove_post(post: praw.models.Submission, reason: str) -> None:
    if REMOVE_POSTS:
        post.mod.remove()
        log(f'Post by /u/{post.author} removed"')
        log(f'Post ID: {post.id}')
        log(f'\nTitle: {post.title}')
        log(f'Flair: {post.link_flair_text}')
        log(f'Link: {post.permalink}')
     
        removal_comment = post.reply(body=reason)
        removal_comment.mod.distinguish()

        send_modmail(post)
    else:
        log(f'Found post violation: "{post.id}" by /u/{post.author}.')
        log(f'Reason: {reason}')
    
def send_modmail(post: praw.models.Submission) -> None:
    modmail_subject = f"I found a post by /u/{post.author} in violation of the rules! Please validate my removal."
    modmail_body = (
        f"I've removed the following post for failing to provide a descriptive title, post body or comment.\n\n"
        f"Title: {post.title}\n"
        f"Author: /u/{post.author}\n\n"
        f"Permalink: {post.permalink}\n"
    )

    # Send the modmail
    post.subreddit.message(modmail_subject, modmail_body)