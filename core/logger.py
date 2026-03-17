import json
import os
from datetime import datetime

LOG_FILE = "logs/logs.json"


def save_log(data):

    os.makedirs("logs", exist_ok=True)

    # load old logs
    if os.path.exists(LOG_FILE):

        with open(LOG_FILE, "r") as f:
            try:
                logs = json.load(f)
            except:
                logs = []

    else:
        logs = []

    # add time
    data["time"] = str(datetime.now())

    logs.append(data)

    # save
    with open(LOG_FILE, "w") as f:
        json.dump(logs, f, indent=2)