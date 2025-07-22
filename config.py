# Facebook Bot Configuration

# Facebook Login Credentials
FB_EMAIL = "lifoin92@gmail.com"  # Replace with your Facebook email
FB_PASSWORD = "lifoin9212@"         # Replace with your Facebook password

# File paths
COOKIES_FILE = "facebook dm/fb-cookies.json"
LOG_FILE = "facebook dm/message_log.csv"
GROUP_LINKS_FILE = "facebook dm/grouplinks.csv"
MESSAGE_FILE = "facebook dm/message.txt"
RESTRICTED_LOG_FILE = "facebook dm/restricted_log.csv"

# Browser settings
CHROME_VERSION = 138  # Chrome version to use
PAGE_LOAD_TIMEOUT = 60  # seconds
LOGIN_TIMEOUT = 50     # seconds

# Messaging settings
MEMBERS_PER_GROUP = 3        # Number of members to message per group
SCROLL_DURATION = 3           # seconds to scroll after login
MIN_DELAY = 3                # minimum delay between messages (seconds)
MAX_DELAY = 10               # maximum delay between messages (seconds)
GROUP_LOAD_DELAY = 7          # delay after loading group page (seconds)
MESSAGE_SEND_DELAY = 5        # delay after sending message (seconds)


# Debug mode
DEBUG = True