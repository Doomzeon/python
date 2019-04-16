import abc
import logging
from message_handler import MessageHandler
from utils import MessageHandlerKey, MessageActionKey


class SourceMessageHandler(MessageHandler):

    def __init__(self, mp_core_queue=None, verbose=False):
        super().__init__(verbose)
        self._logger = logging.getLogger('{}.{}'.format(__name__, type(self).__name__))
        self._mp_core_queue = mp_core_queue
        self._message_dict = {}

    @abc.abstractmethod
    def on_create(self, message_dict):
        ...

    @abc.abstractmethod
    def on_create_event(self, message_dict):
        ...

    @abc.abstractmethod
    def on_create_event_meta(self, message_dict):
        ...

    @abc.abstractmethod
    def on_create_market(self, message_dict):
        ...

    @abc.abstractmethod
    def on_create_odd(self, message_dict):
        ...

    @abc.abstractmethod
    def on_update(self, message_dict):
        ...

    @abc.abstractmethod
    def on_update_event(self, message_dict):
        ...

    @abc.abstractmethod
    def on_update_event_meta(self, message_dict):
        ...

    @abc.abstractmethod
    def on_update_market(self, message_dict):
        ...

    @abc.abstractmethod
    def on_update_odd(self, message_dict):
        ...

    @abc.abstractmethod
    def on_delete(self, message_dict):
        ...

    @abc.abstractmethod
    def on_delete_event(self, message_dict):
        ...

    @abc.abstractmethod
    def on_delete_market(self, message_dict):
        ...

    @abc.abstractmethod
    def on_delete_odd(self, message_dict):
        ...

    @abc.abstractmethod
    def on_commit_event(self, message_dict):
        ...

    def send_message(self, message):
        if message is not None:
            message[MessageHandlerKey.SourceId] = self.source_id
            # self._logger.info("Sending message: {}".format(message))
            self._mp_core_queue.put(message)

    def commit(self):
        if len(self._message_dict):
            self.send_message(self._message_dict)
        self._message_dict = {}

    def create_event_message(self, EventId, InfoDict):
        message_dict = self._get_or_create(MessageActionKey.Create, MessageActionKey.CreateEvent, EventId)
        message_dict.update(SourceMessageHandler._create_template(InfoDict))

    def create_market_message(self, EventId, MarketId, InfoDict):
        message_dict = self._get_or_create(MessageActionKey.Create, MessageActionKey.CreateMarket, EventId, MarketId)
        message_dict.update(SourceMessageHandler._create_template(InfoDict))

    def create_odd_message(self, EventId, MarketId, OddId, InfoDict):
        message_dict = self._get_or_create(MessageActionKey.Create, MessageActionKey.CreateOdd, EventId, MarketId,
                                           OddId)
        message_dict.update(SourceMessageHandler._create_template(InfoDict))

    def create_event_meta_message(self, EventId, InfoDict):
        message_dict = self._get_or_create(MessageActionKey.Create, MessageActionKey.CreateEventMeta, EventId)
        message_dict.update(SourceMessageHandler._create_template(InfoDict))

    def update_event_meta_message(self, EventId, InfoDict):
        message_dict = self._get_or_create(MessageActionKey.Update, MessageActionKey.UpdateEventMeta, EventId)
        message_dict.update(SourceMessageHandler._create_template(InfoDict))

    def create_update_event_message(self, EventId, InfoDict):
        message_dict = self._get_or_create(MessageActionKey.Update, MessageActionKey.UpdateEvent, EventId)
        message_dict.update(SourceMessageHandler._create_template(InfoDict))

    def create_update_market_message(self, EventId, MarketId, InfoDict):
        message_dict = self._get_or_create(MessageActionKey.Update, MessageActionKey.UpdateMarket, EventId, MarketId)
        message_dict.update(SourceMessageHandler._create_template(InfoDict))

    def create_update_odd_message(self, EventId, MarketId, OddId, InfoDict):
        message_dict = self._get_or_create(MessageActionKey.Update, MessageActionKey.UpdateOdd, EventId, MarketId,
                                           OddId)
        message_dict.update(SourceMessageHandler._create_template(InfoDict))

    def create_delete_event_message(self, EventId):
        self._get_or_create(MessageActionKey.Delete, MessageActionKey.DeleteEvent, EventId)

    def create_delete_market_message(self, EventId, MarketId):
        self._get_or_create(MessageActionKey.Delete, MessageActionKey.DeleteMarket, EventId, MarketId)

    def create_delete_odd_message(self, EventId, MarketId, OddId):
        self._get_or_create(MessageActionKey.Delete, MessageActionKey.DeleteOdd, EventId, MarketId, OddId)

    def _get_or_create(self, *component_list):
        node = self._message_dict
        for component in component_list:
            if component not in node:
                node[component] = {}
            node = node[component]
        return node

    @staticmethod
    def _create_template(InfoDict=None):
        template = {}
        if InfoDict is not None:
            template[MessageHandlerKey.Info] = InfoDict
        return template
