from source_message_handler import SourceMessageHandler
import json

class UnibetMessageHandler(SourceMessageHandler):

    def on_create(self, message_dict):
    #       create a json file and insert there JSON data
    #       start
        with open('number_2.json', 'w') as outfile:
            json.dump(json.loads(message_dict),outfile, sort_keys=True, indent=4)
    #       end

    def on_create_event(self, message_dict):
        pass

    def on_create_event_meta(self, message_dict):
        pass

    def on_create_market(self, message_dict):
        pass

    def on_create_odd(self, message_dict):
        pass

    def on_update(self, message_dict):
        pass

    def on_update_event(self, message_dict):
        pass

    def on_update_event_meta(self, message_dict):
        pass

    def on_update_market(self, message_dict):
        pass

    def on_update_odd(self, message_dict):
        pass

    def on_delete(self, message_dict):
        pass

    def on_delete_event(self, message_dict):
        pass

    def on_delete_market(self, message_dict):
        pass

    def on_delete_odd(self, message_dict):
        pass

    def on_commit_event(self, message_dict):
        pass

