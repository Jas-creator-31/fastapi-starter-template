import json
import logging.config
from pathlib import Path


def setup_logging():
    config_file = Path("src/core/logging/logging_config.json")
    if config_file.exists:
        with open(config_file, "rt") as f:
            config = json.load(f)
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(
            filename='app.log',
            filemode='a',
            level=logging.INFO,
            format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
        )