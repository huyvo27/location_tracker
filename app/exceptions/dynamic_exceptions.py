import os
from configparser import ConfigParser

from app.exceptions.base import CustomAPIException

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(BASE_DIR, "exception_config.ini")

config = ConfigParser()
config.read(CONFIG_PATH)

dynamic_exceptions = {}
for section in config.sections():
    class_name = "".join(part.capitalize() for part in section.split("_"))
    status_code = int(config[section]["status_code"])
    code = config[section]["code"]
    message = config[section]["message"]

    def exception_factory(status_code=status_code, code=code, message=message):
        def _init(self, **context):
            super(type(self), self).__init__(status_code, code, message, **context)

        return type(class_name, (CustomAPIException,), {"__init__": _init})

    dynamic_exceptions[class_name] = exception_factory()
