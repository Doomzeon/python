from websocket_manager import WSManager


class UnibetWSManager(WSManager):
    connect_url = 'wss://push.aws.kambicdn.com/socket.io/?EIO=3&transport=websocket'

    # def __init__(self, inbound_queue, outbound_queue):
    # 	super().__init__(inbound_queue, outbound_queue)
    def _build_ws_connect_url(self):
        return UnibetWSManager.connect_url

    def _build_ws_connect_headers(self):
        headers_list = list()
        headers_list.append(('Accept-Encoding', ' gzip, deflate, br'))
        headers_list.append(('User-Agent',
                             ' Mozilla/5.0 headers_list.append((Macintosh; Intel Mac OS X 10_13_1)) AppleWebKit/537.36 headers_list.append((KHTML, like Gecko)) Chrome/65.0.3325.181 Safari/537.36'))
        return headers_list


class UnibetMessageBuilder(object):

    def build_subscribe_event_message(self, event_id):
        return '42["subscribe",{"topic":"v2018.ub.ev.' + str(event_id) + '.json"}]'

    def build_unsubscribe_event_message(self, event_id):
        return '42["unsubscribe",{"topic":"v2018.ub.ev.' + str(event_id) + '.json"}]'
