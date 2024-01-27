
from util import log

def report_post(post, reason):
    post.report(reason)

def remove_post(post, reason):
     post.mod.remove()
     log(f'Removed the post titled "{post.title}" by /u/{post.author}.')
     
     removal_comment = post.reply(body=reason)
     removal_comment.mod.distinguish()