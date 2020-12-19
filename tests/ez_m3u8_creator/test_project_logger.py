import os

from ez_m3u8_creator import project_logger


def test_logging():
    log_dir = R'ez_m3u8_creator\logs'
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    project_logger.setup_logger(R'ez_m3u8_creator\logs\test_log.txt')
    project_logger.test_logging()
