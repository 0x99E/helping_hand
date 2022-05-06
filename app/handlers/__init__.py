from . import task_handler
from . import user_handler
from . import telegram_handler
from . import auth_handler

USER = user_handler
TELEGRAM = telegram_handler
TASK = task_handler
AUTH = auth_handler

__all__ = [
    USER,
    TELEGRAM,
    TASK,
    AUTH,
]