import abc
import logging

class MessageParser(object, metaclass=abc.ABCMeta):
    def __init__(self, message_handler):
        self._message_handler = message_handler
        self._logger = logging.getLogger('{}.{}'.format(__name__, type(self).__name__))

    @abc.abstractmethod
    def parse_message(self, message):
        ...
