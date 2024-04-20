import os
import yaml
import logging
import logging.config
from typing import Optional, Any

LOG_CONFIG_FILE = os.getenv('SCHEDULE_LOG_CONFIG', 'common/log-config.yaml')

_logging_initalised = False

def _initalise_logging() -> None:
    global _logging_initalised

    if not _logging_initalised:
        with open(LOG_CONFIG_FILE) as file:
            logging.config.dictConfig(yaml.safe_load(file))
        _logging_initalised = True


class ScheduleLogger:
    def __init__(self, name: Optional[str] = None) -> None:
        _initalise_logging()
        self._logger = logger = logging.getLogger(name)

    def __getattr__(self, name: str) -> Any:
        if hasattr(self._logger, name):
            return getattr(self._logger, name)
        else:
            raise AttributeError('Logging module has no attributes {}'.format(name))