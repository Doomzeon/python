import requests
import asyncio
import json
import logging
from unibet_websocket import UnibetWSManager
from unibet_websocket import UnibetMessageBuilder
from unibet_utils import UnibetKey
from unibet_message_handler import UnibetMessageHandler
from unibet_parser import UnibetMessageParser
import websocket

class Unibet:
    # get_in_play_match_url='https://e4-api.kambi.com/offering/api/v3/ub/listView/all/all/all/all/in-play.json?lang=en_GB&market=ZZ'

    live_vents_url = 'https://e1-api.aws.kambicdn.com/offering/api/v2/ub/event/live/open.json?lang=en_GB&market=ZZ'
    #live_vents_url = 'wss://push.aws.kambicdn.com/socket.io/?EIO=3&transport=websocket'
    #
##

    def __init__(self):
        self._logger = logging.getLogger('{}.{}'.format(__name__, type(self).__name__))
        self.__keep_running = True
        self.__keep_syncing_events = True
        self.__inbound_queue = asyncio.Queue()
        self.__outbound_queue = asyncio.Queue()
        self.__message_builder = UnibetMessageBuilder()
        self.__event_id_set = set()

    async def loop(self):
        while self.__keep_running:
            try:
                unibet_ws = UnibetWSManager(self.__inbound_queue, self.__outbound_queue)
                unibet_ws.start()
                message_parser = UnibetMessageParser(UnibetMessageHandler(True))
                asyncio.ensure_future(self.sync_events())

                while self.__keep_running:
                    message = await self.__inbound_queue.get()
                    if message is not None:
                        message_parser.parse_message(message)
                        self.__inbound_queue.task_done()

            except Exception as e:
                self._logger.error(e)

    async def sync_events(self):
        try:
            while self.__keep_syncing_events:
                event_id_set = Unibet.retrieve_events_list()
                new_event_id_set = event_id_set - self.__event_id_set
                closed_event_id_set = self.__event_id_set - event_id_set
                for new_event_id in new_event_id_set:
                    register_event_message = self.__message_builder.build_subscribe_event_message(new_event_id)
                    self.__outbound_queue.put_nowait(register_event_message)
                for closed_event_id in closed_event_id_set:
                    unregister_event_message = self.__message_builder.build_unsubscribe_event_message(closed_event_id)
                    self.__outbound_queue.put_nowait(unregister_event_message)
                self.__event_id_set = event_id_set
                await asyncio.sleep(30)
        except Exception as e:
            self._logger.error(e)

    @staticmethod
    def retrieve_events_list():

        event_id_list = set()
        try:
            response_data = requests.get(Unibet.live_vents_url)
            #print("Events: "+str(response_data.content))
            if response_data is not None:
                events_dict = json.loads(response_data.content)
                if events_dict is not None and UnibetKey.liveEvents in events_dict:
                    for event_obj in events_dict[UnibetKey.liveEvents]:
                        if UnibetKey.event in event_obj:
                            event = event_obj[UnibetKey.event]
                            if event is not None and UnibetKey._id in event:
                                event_id_list.add(event[UnibetKey._id])
                else:
                    print("events dict is none")
        except Exception as e:
            print("Unable to retrieve envet list - error: " + str(e))

        return event_id_list


if __name__ == '__main__':
    unibet = Unibet()
    asyncio.get_event_loop().run_until_complete(unibet.loop())
