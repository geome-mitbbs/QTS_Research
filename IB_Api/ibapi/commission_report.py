"""
Copyright (C) 2016 Interactive Brokers LLC. All rights reserved.  This code is
subject to the terms and conditions of the IB API Non-Commercial License or the
 IB API Commercial License, as applicable. 
"""

from ibapi.object_implem import Object 


class CommissionReport(Object):

    def __init__(self):
        self.execId = ""
        self.commission = 0. 
        self.currency = ""
        self.realizedPNL =  0.
        self.yield_ = 0.
        self.yieldRedemptionDate = 0  # YYYYMMDD format

    def __str__(self):
        s = "%s: %f %s %f %f %d" % (self.execId, self.commission, 
            self.currency, self.realizedPNL, self.yield_, 
            self.yieldRedemptionDate)
        return s
 
