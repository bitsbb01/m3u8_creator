#!/usr/bin/env python3

"""POC Module."""

import logging.config

logger = logging.getLogger(__name__)  # pylint: disable=invalid-name


def setup_logger(log_file_path: str) -> None:
    """Set up module logging."""
    logger_dict = {
        'version': 1,
        'formatters': {
            'default': {'format': '%(asctime)s - %(filename)s:%(funcName)s():'
                                  '%(lineno)i: %(levelname)s - %(message)s',
                        'datefmt': '%Y-%m-%d %H:%M:%S'}
        },
        'handlers': {
            'console': {
                'level': 'INFO',
                'class': 'logging.StreamHandler',
                'formatter': 'default'
            },
            'file': {
                'level': 'DEBUG',
                'class': 'logging.handlers.RotatingFileHandler',
                'formatter': 'default',
                'filename': log_file_path,
                'maxBytes': 5242880,
                'backupCount': 1
            }
        },
        'loggers': {
            '': {
                'level': 'DEBUG',
                'handlers': ['console', 'file'],
                'propagate': True
            }
        },
        'disable_existing_loggers': False
    }
    logging.config.dictConfig(logger_dict)


def test_logging() -> None:
    """Test the logging."""
    logger.debug('debug message!')
    logger.info('info message!')
    logger.error('error message')
    logger.critical('critical message')
    logger.warning('warning message')


def main() -> None:
    """Our Main function."""
    setup_logger('log.log')
    test_logging()


if __name__ == '__main__':
    main()
