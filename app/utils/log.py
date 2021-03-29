import logging
import logging.config
from typing import Any, Dict

DEFAULT_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'INFO',
            'formatter': 'default'
        },
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': 'WARNING',
            'formatter': 'default',
            'maxBytes': 1e6,
            'filename': 'store/log.txt',
            'backupCount': 3
        },
    },
    'formatters': {
        'default': {
            'format': '%(asctime)s %(levelname)-8s: %(name)s - %(message)s',
        }
    },
    'loggers': {
        '': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': True
        }
    }
}


def configure_logging(config: Dict[str, Any] = None) -> None:
    """ Configure logging with dict of settings. """
    if config is None:
        config = DEFAULT_CONFIG
    logging.config.dictConfig(config)
