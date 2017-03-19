"""
Copyright (C) 2016 Interactive Brokers LLC. All rights reserved.  This code is
subject to the terms and conditions of the IB API Non-Commercial License or the
 IB API Commercial License, as applicable. 
"""



from ibapi.object_implem import Object


class Execution(Object):

    def __init__(self):
        self.execId = ""
        self.time =  ""
        self.acctNumber =  ""
        self.exchange =  ""
        self.side = ""
        self.shares = 0.
        self.price = 0. 
        self.permId = 0
        self.clientId = 0
        self.orderId = 0
        self.liquidation = 0
        self.cumQty = 0.
        self.avgPrice = 0.
        self.orderRef =  ""
        self.evRule =  ""
        self.evMultiplier = 0.
        self.modelCode =  ""

    def __str__(self):
        return ",".join((
            str(self.execId),
            str(self.time),
            str(self.acctNumber),
            str(self.exchange),
            str(self.side),
            str(self.shares),
            str(self.price),
            str(self.permId),
            str(self.clientId),
            str(self.orderId),
            str(self.liquidation),
            str(self.cumQty),
            str(self.avgPrice),
            str(self.orderRef),
            str(self.evRule),
            str(self.evMultiplier),
            str(self.modelCode)))
     

class ExecutionFilter(Object):

    # Filter fields
    def __init__(self):
        self.clientId = 0
        self.acctCode = ""
        self.time = ""
        self.symbol = ""
        self.secType = ""
        self.exchange = "" 
        self.side = ""

