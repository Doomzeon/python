from parser import MessageParser
from utils import AutoDict
from message_handler import MessageHandler

from unibet_utils import UnibetKey


class UnibetMessageParser(MessageParser):

    def __init__(self, message_handler=None):
        super().__init__(message_handler)

    def parse_message(self, message):
        verbose = False
        try:
            if message is not None:
                if message[:2] == '42':
                    message_purged = message[2:]
                    message_dict = AutoDict.json_loads(message_purged)
                    if len(message_dict) >= 2 and message_dict[0] == 'message':
                        inner_message = message_dict[1]
                        inner_message_dict = AutoDict.json_loads(inner_message)

                        for element_dict in inner_message_dict:
                            if UnibetKey.boou in element_dict:  # odds update
                                boou = element_dict[UnibetKey.boou]
                                if verbose or True:

                                    print("BOOU " + boou.dumps())
                                    boou_copy = boou.copy()

                                    self.__call_on_update_cb(boou_copy)

                                    self._message_handler.on_create(boou.dumps())

                            elif UnibetKey.boa in element_dict:  # odd add
                                boa = element_dict[UnibetKey.boa]
                                if verbose:
                                    print("BOA " + boa.dumps())
                                    boa_copy = boa.copy()
                                    self.__call_on_insert_cb(boa_copy)  #O. V.
                            elif UnibetKey.booa in element_dict:  # odd add
                                booa = element_dict[UnibetKey.booa]
                                if verbose:
                                    print("BOOA " + booa.dumps())
                                    booa_copy = booa.copy()
                                    self.__call_on_insert_cb(booa_copy)
                            elif UnibetKey.bosu in element_dict:  # odd suspend
                                bosu = element_dict[UnibetKey.bosu]
                                if verbose:
                                    print("BOSU " + bosu.dumps())
                            elif UnibetKey.bor in element_dict:  # section remove
                                bor = element_dict[UnibetKey.bor]
                                bor_copy = bor.copy()
                                if verbose:
                                    print("BOR " + bor_copy.dumps())
                                    self.__call_on_delete_cb(bor_copy)
                            elif UnibetKey.boor in element_dict:  # odd remove
                                boor = element_dict[UnibetKey.bor]
                                boor_copy = boor.copy()
                                if verbose:
                                    print("BOOR " + boor_copy.dumps())
                                    self.__call_on_delete_cb(boor_copy)
                            elif UnibetKey.vo in element_dict:  # event metadata
                                if verbose:
                                    print("VO " + element_dict[UnibetKey.vo].dumps())
                            elif UnibetKey.mo in element_dict:  # event metadata
                                if verbose:
                                    print("MO " + element_dict[UnibetKey.mo].dumps())
                            elif UnibetKey.mcu in element_dict:  # event metadata
                                if verbose:
                                    print("MCU " + element_dict[UnibetKey.mcu].dumps())
                            elif UnibetKey.score in element_dict:  # score update
                                if verbose:
                                    print("SCORE " + element_dict[UnibetKey.score].dumps())
                            elif UnibetKey.tu in element_dict:  # event metadata
                                if verbose:
                                    print("TU " + element_dict[UnibetKey.tu].dumps())
                            elif UnibetKey.os in element_dict:  # event metadata
                                if verbose:
                                    print("OS " + element_dict[UnibetKey.os].dumps())
                            else:
                                print("Unknwon message: " + element_dict.dumps())

        except Exception as e:
            self._logger.error(e)

    # print("Parse exception: "+str(e))

    def __call_on_insert_cb(self, message_dict):
        self._message_handler.on_insert(message_dict)

    def __call_on_update_cb(self, message_dict):
        self._message_handler.on_update(message_dict)

    def __call_on_delete_cb(self, message_dict):
        self._message_handler.on_delete(message_dict)

# O.V create JSON file of info
    def __create_json_file(self, message_dict):
        self._message_handler.on_create(message_dict)
