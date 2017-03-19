"""
Copyright (C) 2016 Interactive Brokers LLC. All rights reserved.  This code is
subject to the terms and conditions of the IB API Non-Commercial License or the
 IB API Commercial License, as applicable.
"""

import sys

from ibapi.enum_implem import Enum
from ibapi.object_implem import Object


NO_VALID_ID = -1
MAX_MSG_LEN = 0xFFFFFF # 16Mb - 1byte

UNSET_INTEGER = 2 ** 31 - 1
UNSET_DOUBLE = sys.float_info.max

TickerId = int
OrderId  = int
TagValueList = list

FaDataType = int
FaDataTypeEnum = Enum("N/A", "GROUPS", "PROFILES", "ALIASES")

MarketDataType = int
MarketDataTypeEnum = Enum("N/A", "REALTIME", "FROZEN", "DELAYED", "DELAYED_FROZEN")

SetOfString = set
SetOfFloat = set
ListOfOrder = list
ListOfFamilyCode = list
ListOfContractDescription = list
ListOfDepthExchanges = list
ListOfNewsProviders = list
SmartComponentMap = dict
HistogramData = list

class BarData(Object):
    def __init__(self):
        self.date = ""
        self.open = 0.
        self.high = 0.
        self.low = 0.
        self.close = 0.
        self.volume = 0
        self.average = 0.
        self.hasGaps = ""
        self.barCount = 0


    def __str__(self):
        return "%s:%f,%f,%f,%f,%d,%f,%s,%d" % (self.date, self.open, self.high,
            self.low, self.close, self.volume, self.average, self.hasGaps,
            self.barCount)

class HistogramData(Object):
    def __init__(self):
        self.price = 0.
        self.count = 0

    def __str__(self):
        return "%f,%d" % (self.price,self.count)

class NewsProvider(Object):
    def __init__(self):
        self.code = ""
        self.name = ""

    def __str__(self):
        return "%s, %s" % (self.code, self.name)

class DepthMktDataDescription(Object):
    def __init__(self):
        self.exchange = ""
        self.secType = ""
        self.listingExch = ""
        self.serviceDataType = ""
        self.aggGroup = UNSET_INTEGER

    def __str__(self):
        if (self.aggGroup!= UNSET_INTEGER):
            aggGroup = self.aggGroup
        else:
            aggGroup = ""
        return "%s,%s,%s,%s,%s" % (self.exchange, self.secType, self.listingExch,self.serviceDataType, aggGroup)

class SmartComponentsMap(Object):
    def __init__(self):
        self.bitNumber = 0
        self.exchange = ""
        self.exchangeLetter = ""

    def __str__(self):
        return "%d,%s,%s" % (self.bitNumber,self.exchange,self.exchangeLetter)

class TickAttrib(Object):
    def __init__(self):
        self.canAutoExecute = False
        self.pastLimit = False

    def __str__(self):
        return "%d,%d" % (self.canAutoExecute, self.pastLimit)


class FamilyCode(Object):
    def __init__(self):
        self.accountID = ""
        self.familyCodeStr = ""

    def __str__(self):
        return "%s,%s" % (self.accountID, self.familyCodeStr)


