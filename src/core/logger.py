import logging.config

import yaml


def init_log_config():
    with open("core/log_config.yml", "r", encoding="utf-8") as f:
        config = yaml.safe_load(f.read())
        logging.config.dictConfig(config)


auth_logger = logging.getLogger("auth_logger")
