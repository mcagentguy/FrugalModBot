# config.py
# Here lies secrets

# Reddit bots are 'Reddit apps'. https://www.reddit.com/prefs/apps
#
# Reddit apps make requests to Reddit's API via OAuth.
# 
# https://github.com/reddit-archive/reddit/wiki/OAuth2
#

# Reddit apps require a client ID and client secret.

''' PRAW setup '''

# Tells reddit.com which app is making the request
CLIENT_ID = 'GouOLoJd3E3is2fdIU3ANQ'

# A user agent is a string of text that is sent with HTTP requests
# to identify the program making the request.
USER_AGENT = 'FrugalModBot'

# reddit account. Do not include the u/. Example: "mcagent" or "FrugalModBot"
REDDIT_USERNAME = 'FrugalModBot'

# Subreddit to run on. Do not include the r/. Examples: "Frugal" or "FrugalTest"
TARGET_SUBREDDIT = 'Frugal'

''' Configuarations '''

# These are extensions the bot looks for in self posts. If one of these is found,
# the post will be treated as a link post.
IMAGE_EXTENSIONS = ['.png', '.jpg', '.jpeg', '.gif']

# The length a comment (in characters) must be to prevent it from triggering a mod report.
COMMENT_CHARACTER_MINIMUM = 150

# The length a self post (with an image extension) must be to prevent a report.
POST_CHARACTER_MINIMUM = 150

# The length a title must be to avoid a report.
POST_TITLE_CHARACTER_MINIMUM = 150

# When the remove a post due to comment size (if title and body are also too short)
COMMENT_LENGTH_REMOVAL = 80

# When to remove a post due to title length (if comment and body are also too short)
TITLE_LENGTH_REMOVAL = 80

# This value is in minutes. If you want 30 minutes, put 30 here. If you want 2 hours, put 120 here.
POST_AGE_BEFORE_BOT_CHECKS_COMMENTS = 8

# These are the debug messages that show up in both the FrugalModBot.log file and the terminal.
ENABLE_DEBUG_MESSAGES = False

# Set to True and the bot will remove posts. Set to false and the bot will simply log violations instead.
REMOVE_POSTS = True

# Secrets & passwords are stored in credentials.py.