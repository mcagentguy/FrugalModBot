
import praw
import config

# This message shows up at the bottom of removal comments from the bot.
BOT_MESSAGE_SUFFIX = '''
If you would like to appeal this decision, please [message the moderators by clicking this link](http://www.reddit.com/message/compose?to=%2Fr%2FFrugal&subject=Removal%20Appeal&message=Author%20would%20like%20to%20appeal%20the%20removal%20of%20their%20post%20because) within one week of this notice being posted
'''

# This is the report reason when an OP leaves a short comment on their image post.
SHORT_COMMENT_REPORT_REASON = "OP left a short comment on an image post. Please review."

# This is the report reason when an OP creates a self post with an image without a long enough description.
SHORT_POST_REPORT_REASON = "Image post without"

def FOLLOW_UP_OR_POORLY_DESCRIPTIVE_POST_REASON(post: praw.models.Comment) -> str:
    """
    post: praw.models.Submission
    """
    return (f"Hi {post.author}, thanks for contributing. However, your [submission]({post.permalink}) was removed from /r/{config.TARGET_SUBREDDIT}.\n"
            f"\nWe are removing your post/comment because the content needs a follow-up comment or is poorly descriptive. This usually happens because: \n"
            f"\n- You created an image post but did not accompany it with a relevant top-level comment. \n"
            f"\n- If you posted something you made, there was no top-level comment explaining how you made it, how much time it took, how much it cost, share the recipe/build, etc."
            f"\n- You shared a success story but did not share how you succeeded.\n"
            f"\n Please see our full rules page for the specifics. https://www.reddit.com/r/Frugal/about/rules/"
            f"\n{BOT_MESSAGE_SUFFIX}")