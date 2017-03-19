"""
Copyright (C) 2016 Interactive Brokers LLC. All rights reserved.  This code is
subject to the terms and conditions of the IB API Non-Commercial License or the
 IB API Commercial License, as applicable. 
"""


from ibapi.object_implem import Object
from ibapi.common import UNSET_INTEGER, UNSET_DOUBLE


class ScanData(Object):
    def __init__(self):
        self.contract = None
        self.rank = 0
        self.distance = ""
        self.benchmark = ""
        self.projection = ""
        self.legsStr = ""

    def __str__(self):
        return "%s,%d,%s,%s,%s,%s" % (self.contract, self.rank, self.distance,
            self.benchmark, self.projection, self.legsStr)
 
NO_ROW_NUMBER_SPECIFIED = -1

class ScannerSubscription(Object):

    def __init__(self):
        self.numberOfRows = NO_ROW_NUMBER_SPECIFIED
        self.instrument = ""
        self.locationCode = ""
        self.scanCode =  ""
        self.abovePrice = UNSET_DOUBLE
        self.belowPrice = UNSET_DOUBLE
        self.aboveVolume = UNSET_INTEGER
        self.marketCapAbove = UNSET_DOUBLE
        self.marketCapBelow = UNSET_DOUBLE
        self.moodyRatingAbove =  ""
        self.moodyRatingBelow =  ""
        self.spRatingAbove =  ""
        self.spRatingBelow =  ""
        self.maturityDateAbove =  ""
        self.maturityDateBelow =  ""
        self.couponRateAbove = UNSET_DOUBLE
        self.couponRateBelow = UNSET_DOUBLE 
        self.excludeConvertible = 0
        self.averageOptionVolumeAbove = UNSET_INTEGER
        self.scannerSettingPairs =  ""
        self.stockTypeFilter =  ""


    def __str__(self):
        s = "%s,%s,%s" % (self.instrument, self.locationCode, self.scanCode)

        return s

