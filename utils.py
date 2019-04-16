import copy
import json
import os
from collections.abc import MutableMapping
from json import JSONEncoder



class TranslationKey:
    Competitor1 = "competitor1"
    Competitor2 = "competitor2"
    Competitor1Full = "competitor1Full"
    Competitor2Full = "competitor2Full"
    EventMetas = 'EventMetas'
    Id = "Id"
    Key = "Key"
    MARKETS_RE = 'MARKETS_RE'
    DefaultMargin = 'DefaultMargin'
    MapName = 'MapName'
    Market = "Market"
    MarketNameRE = "MarketNameRE"
    Markets = "Markets"
    MarketsDictionary = "MarketsDictionary"
    MatchStatus = "MatchStatus"
    Metas = 'Metas'
    Name = "Name"
    ODDS_RE = 'ODDS_RE'
    Odds = "Odds"
    OddsDictionary = "OddsDictionary"
    Periods = "Periods"
    RE = 'RE'
    SourceSportId = 'SourceSportId'
    Specs = 'Specs'
    Sports = "Sports"


class MasterKey(object):
    pass


class EventKey(MasterKey):
    Markets = 'Markets'
    Meta = 'Meta'
    Odds = 'Odds'
    Specs = 'Specs'
    Suspended = 'susp'
    Value = 'V'


class EventMetaKey(EventKey):
    FirstToScore = 'FirstToScore'
    LastToScore = 'LastToScore'
    EventScore = 'EventScore'
    Periods = 'Periods'
    PeriodId = 'Period'
    Running = 'Run'
    Seconds = 'Seconds'
    Timer = 'Timer'
    Total = 'Total'


class BREventMetaKey:
    score = 'score'
    yellow_cards = 'yellow_cards'
    red_cards = 'red_cards'
    yellow_red_cards = 'yellow_red_cards'
    corners = 'corners'
    timer = 'timer'
    period = 'period'

class MessageActionKey:
    # Source management
    CreateSource = "CreateSource"

    # Tree management

    Create = "C"
    CreateEvent = "CE"
    CreateEventMeta = "CEM"
    CreateMarket = "CM"
    CreateOdd = "CO"

    Delete = "D"
    DeleteEvent = "DE"
    DeleteMarket = "DM"
    DeleteOdd = "DO"

    Update = "U"
    UpdateOdd = "UO"
    UpdateMarket = 'UM'
    UpdateEvent = 'UE'
    UpdateEventMeta = 'UEM'

    CommitEvent = 'CommitEvent'


class MessageType:
    ACK = 'ACK'
    Management = 'MNGMNT'
    Regular = 'R'


class MessageKey:
    Action = 'Action'
    EventId = 'EventId'
    Info = 'Info'
    MarketId = 'MarketId'
    MarketsList = 'MarketsList'
    OddId = 'OddId'
    OddsList = 'OddsList'
    Path = 'Path'
    SourceId = 'SourceId'
    Sport = 'Sport'
    Suspend = 'Suspend'
    Type = 'Type'
    Value = 'Value'


class MessageHandlerKey(MessageKey):
    pass


class EventNotFoundException(Exception):
    pass


def mkdirp(path):
    wdir = None
    for element in path.split('/'):
        wdir = element if wdir is None else wdir + '/' + element
        try:
            os.stat(wdir)
        except FileNotFoundError as e:
            if len(wdir) > 0:
                os.mkdir(wdir)
    return wdir




class AutoDict(MutableMapping):
    def __init__(self, raw_dict=None):
        if raw_dict:
            if hasattr(raw_dict, '__class__') and issubclass(raw_dict.__class__, AutoDict):
                self.__inner_dict = raw_dict.__get_inner_dict()
            else:
                self.__inner_dict = raw_dict
        else:
            self.__inner_dict = dict()

    def __getitem__(self, key):
        if key in self.__inner_dict:
            return self.__inner_dict[key]

        new_dict = AutoDict()
        self.__inner_dict[key] = new_dict
        return new_dict

    def __contains__(self, key):
        return key in self.__inner_dict

    def __iter__(self):
        return iter(self.__inner_dict)

    def __len__(self):
        return len(self.__inner_dict)

    def __delitem__(self, key):
        del (self.__inner_dict[key])

    def __setitem__(self, key, value):
        self.__inner_dict[key] = value

    def __get_inner_dict(self):
        return self.__inner_dict

    def __deepcopy__(self, d):
        return AutoDict(copy.deepcopy(self.__inner_dict, d))

    def __str__(self):
        return self.__inner_dict.__str__()

    def __repr__(self):
        return self.__inner_dict.__repr__()

    def deepcopy(self):
        return copy.deepcopy(self)

    def copy(self):
        return self.deepcopy()

    def to_dict(self):
        root_dict = {}
        for k, v in self.__inner_dict.items():
            if issubclass(type(v), AutoDict):
                v = v.to_dict()
            root_dict[k] = v
        return root_dict

    def update(self, other_dict):
        for k, v in other_dict.items():
            self.__inner_dict[k] = v

    def dumps(self):
        return json.dumps(self, cls=AutoDictJSEncoder, separators=(',', ':'))

    def get_serializable_object(self):
        return self.__inner_dict

    @staticmethod
    def json_loads(json_string):
        return json.loads(json_string, object_hook=lambda obj: AutoDict(obj))


class AutoDictJSEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, AutoDict):
            return o.get_serializable_object()
        return JSONEncoder.default(self, o)
