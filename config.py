from dotenv import load_dotenv
import os

# Globals

# List of companies for which alerts should not be sent.
# Company name should match the name shown in the logs exactly.
# Effective only when MONITOR_ALL_EXCEPT_BLACKLIST = True.
ALERT_BLACKLIST = []

# List of companies for which alerts should be sent.
# Company name should match the name shown in the logs exactly.
# Effective only when MONITOR_ALL_EXCEPT_BLACKLIST = False.
ALERT_WHITELIST = []

# Partner company catalog URL where interview slots are opened.
CATALOG_URL = "https://gracehoppercelebration.com/flow/anitab/vcf25/exhcatalog/page/ghc25sponsorcatalog"

# Link to this project's GitHub
GITHUB_URL = "https://github.com/jaswaniyogita/GHC_InterviewSlotAvailability"

# Event name for the IFTTT applet
IFTTT_EVENT_NAME = "ghc25vcfalert"

# IFTTT keys of accounts that will receive push notifications
IFTTT_KEYS = None

# API to send push notifications through IFTTT
IFTTT_URL = f"https://maker.ifttt.com/trigger/{IFTTT_EVENT_NAME}/json/with/key/"

# Controls which companies are monitored for alerts
#
# - If True:
#   - Monitor every company in the catalog.
#   - No alerts are sent for companies listed in ALERT_BLACKLIST.
#   - ALERT_WHITELIST is ignored (has no effect).
#
# - If False:
#   - Only companies in ALERT_WHITELIST are monitored.
#   - ALERT_BLACKLIST is ignored (has no effect).
#
# Related variables: ALERT_BLACKLIST, ALERT_WHITELIST
MONITOR_ALL_EXCEPT_BLACKLIST = True

# API to send push notifications through Pushbullet
PUSHBULLET_URL = "https://api.pushbullet.com/v2/pushes"

# Pushbullet access tokens
PUSHBULLET_TOKENS = None

# Pushbullet tokens for testing and error alerts
PUSHBULLET_TESTING_AND_ERROR_TOKENS = None

# Time in seconds for which the script goes to sleep after
# one round of monitoring the catalog, to avoid overloading
# the server
SCRIPT_SLEEP_DURATION = 3600

# Dynamic config load


def load_values(key):
    """Reads access tokens from .env file. For instructions, visit: {GITHUB_URL}"""
    tokens_str = os.getenv(key, "")
    tokens_list = tokens_str.split(";") if tokens_str else []
    print(f"Found {len(tokens_list)} values for {key}.")
    return tokens_list


# If config.py is run directly
if __name__ == "__main__":
    print(f"Run main.py instead. For instructions, visit: {GITHUB_URL}")
else:
    load_dotenv()
    IFTTT_KEYS = load_values("IFTTT_KEYS")
    PUSHBULLET_TOKENS = load_values("PUSHBULLET_ACCESS_TOKENS")
    PUSHBULLET_TESTING_AND_ERROR_TOKENS = load_values(
        "PUSHBULLET_ACCESS_TOKENS_TESTING_AND_ERRORS"
    )
