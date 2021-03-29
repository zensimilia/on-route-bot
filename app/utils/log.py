import logging
import logging.config
from typing import Any, Dict

DEFAULT_CONFIG: Dict[str, Any] = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'INFO',
            'formatter': 'default'
        },
    },
    'formatters': {
        'default': {
            'format': '%(asctime)s %(levelname)-8s: %(name)s - %(message)s',
        }
    },
    'loggers': {
        '': {
            'handlers': ['console'],
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
