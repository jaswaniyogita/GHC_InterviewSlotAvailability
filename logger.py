from datetime import datetime
import logging
import os


class ColorFormatter(logging.Formatter):
    COLORS = {
        logging.DEBUG: "\033[97m",  # White
        logging.INFO: "\033[97m",  # White
        logging.WARNING: "\033[97m",  # White
        logging.ERROR: "\033[91m",  # Red
        logging.CRITICAL: "\033[30;103m",  # Bright yellow background, black text
    }
    RESET = "\033[0m"

    def format(self, record):
        color = self.COLORS.get(record.levelno, self.RESET)
        message = super().format(record)
        return f"{color}{message}{self.RESET}"


# --- Console Handler ---
console_handler = logging.StreamHandler()
console_handler.setFormatter(
    ColorFormatter("%(asctime)s [%(levelname)s] %(message)s", "%Y-%m-%d %H:%M:%S")
)

# --- File Handler ---
os.makedirs("logs", exist_ok=True)
now = datetime.now()
formatted = now.strftime("%Y-%m-%d-%H-%M-%S")
file_handler = logging.FileHandler(
    os.path.join("logs", f"{formatted}.log"), encoding="utf-8"
)
file_handler.setFormatter(
    logging.Formatter("%(asctime)s [%(levelname)s] %(message)s", "%Y-%m-%d %H:%M:%S")
)

# --- Logger Setup ---
logger = logging.getLogger("ghc_monitor")
logger.handlers = []  # clear any existing handlers
logger.addHandler(console_handler)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)
