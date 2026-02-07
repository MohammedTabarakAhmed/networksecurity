import logging
import os
from datetime import datetime

LOG_FILE=f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"

logs_path=os.path.join(os.getcwd(),"LOGS")
os.makedirs(logs_path,exist_ok=True)

LOG_FILE_PATH=os.path.join(logs_path,LOG_FILE)

logging.basicConfig( #- Record INFO, WARNING, ERROR, and CRITICAL messages.
                    # - Ignore DEBUG messages (they’re too detailed unless you’re debugging).
    filename=LOG_FILE_PATH,
    format="[%(asctime)s] [line:%(lineno)d] [%(name)s] - %(levelname)s - %(message)s",
    level=logging.INFO
)