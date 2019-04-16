import abc
import logging


class MessageHandler(object, metaclass=abc.ABCMeta):

    def __init__(self, verbose=False):
        super().__init__()
        self._verbose = verbose
        self._logger = logging.getLogger('{}.{}'.format(__name__, type(self).__name__))
