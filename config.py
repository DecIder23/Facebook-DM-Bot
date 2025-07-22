# Facebook Bot Configuration

# Facebook Login Credentials
FB_EMAIL = "example@gmail.com"  # Replace with your Facebook email
FB_PASSWORD = "enteryourpassword"         # Replace with your Facebook password

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
MEMBERS_PER_GROUP = 10        # Number of members to message per group
SCROLL_DURATION = 3           # seconds to scroll after login
MIN_DELAY = 15                # minimum delay between messages (seconds)
MAX_DELAY = 60               # maximum delay between messages (seconds)
GROUP_LOAD_DELAY = 7          # delay after loading group page (seconds)
MESSAGE_SEND_DELAY = 5        # delay after sending message (seconds)


# Debug mode
DEBUG = True
