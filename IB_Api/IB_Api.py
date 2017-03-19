# to implement very basic operations through ib
from ibapi import wrapper
from ibapi.client import EClient
from ibapi.contract import *
from ibapi.order import Order

class IB_Api(wrapper.EWrapper,EClient):
    def __init__(self):
        wrapper.EWrapper.__init__(self)
        EClient.__init__(self, wrapper=self)
        self.nextValidOrderId = None

    def connect_to_ib(self):
        self.connect("127.0.0.1", 7497, clientId=0)
        print("serverVersion:%s connectionTime:%s" % (self.serverVersion(),self.twsConnectionTime()))

    def buy(self,ticker,qty):
        self.placeOrder(self.get_next_order_id(), self.get_contract(ticker),self.get_order("BUY", qty))
        pass

    def sell(self,ticker,qty):
        self.placeOrder(self.get_next_order_id(), self.get_contract(ticker),self.get_order("SELL", qty))
        pass

    def get_contract(self,ticker):
        contract = Contract()
        contract.symbol = ticker
        contract.secType = "STK"
        contract.currency = "USD"
        contract.exchange = "SMART"
        return contract

    def get_order(self,action:str, quantity:float):
        order = Order()
        order.action = action
        order.orderType = "MKT"
        order.totalQuantity = quantity
        return order

    def get_next_order_id(self):
        orig_id = self.nextValidOrderId
        self.nextValidOrderId += 1
        return orig_id

    def nextValidId(self, orderId: int):
        super().nextValidId(orderId)
        self.nextValidOrderId = orderId
        self.start()

    def start(self):
        app.buy("AAPL",100)
        app.sell("MSFT",100)
        app.buy("GOOG",100)
        app.done = True

# Simple example of usage
# app = IB_Api()
# app.connect_to_ib()
# app.run()
