import numpy as np
try:
    from . import Quant_Indicators as QI
    from . import Data_API
except:
    import Quant_Indicators as QI
    import Data_API
    

class Portfolio:
    def __init__(self,init_cash_amt=0,init_pos=None,allow_short_cash=False,allow_short_sell=True):
        self.pnl_as_of_date = []
        if init_pos==None:
            self.current_portfolio = {'cash':init_cash_amt+0.0}
        else:
            self.current_portfolio = init_pos
        self.trade_list = []
        self.allow_short_cash = allow_short_cash
        self.allow_short_sell = allow_short_sell
        
    def buy(self,ticker,qty=None,value=None,percent=None,price_feature='Close'):
        if not QI.is_biz_day(ticker):
            return
        if(qty==None and value==None and percent==None):
            percent = 1
        
        unit_px = QI.price(ticker,price_feature=price_feature)
        if(qty!=None and value!=None)or(qty!=None and percent!=None)or(value!=None and percent!=None):
            raise Exception('qty value percent specified more than once')
        if(value!=None):
            qty = value/unit_px
        if(percent!=None):
            qty = self.current_portfolio['cash'] * percent/unit_px

        if (self.current_portfolio['cash'] - unit_px *qty) < 0 and (not self.allow_short_cash):
            return

        self.current_portfolio['cash'] -= unit_px * qty
        if ticker in self.current_portfolio.keys():
            self.current_portfolio[ticker] += qty
        else:
            self.current_portfolio[ticker] = qty
        self.trade_list.append(("buy", ticker, qty, unit_px))

    def sell(self,ticker,qty=None,value=None,percent = None,price_feature='Close'):
        if not QI.is_biz_day(ticker):
            return
        if(qty==None and value==None and percent==None):
            percent = 1
        
        unit_px = QI.price(ticker,price_feature=price_feature)
        if(qty!=None and value!=None)or(qty!=None and percent!=None)or(value!=None and percent!=None):
            raise Exception('qty value percent specified more than once')
        if(value!=None):
            qty = value/unit_px
        if(percent!=None):
            if ticker in self.current_portfolio.keys():
                qty = self.current_portfolio[ticker] * percent
            else:
                return
        
        if(not self.allow_short_sell):
            if not (ticker in self.current_portfolio.keys()):
                return
            elif (self.current_portfolio[ticker] - qty) < 0:
                return
                
        self.current_portfolio['cash'] += unit_px * qty
        if ticker in self.current_portfolio.keys():
            self.current_portfolio[ticker] -= qty
        else:
            self.current_portfolio[ticker] = -qty
        self.trade_list.append(("sell", ticker, qty, unit_px))

    def value(self):
        pnl = 0
        for key in self.current_portfolio:
            if(key=="cash"):
                pnl += self.current_portfolio[key]
            else:
                pnl += self.current_portfolio[key] * QI.price(key)
        return pnl

    def get_measures(self):
        ret = dict()
        ts = np.array([x[1] for x in self.pnl_as_of_date])
        ret['return']="{0:.4f}".format(QI.price_return(ts))
        ret['volatility']="{0:.4f}".format(QI.volatility(ts),4)
        ret['draw_down']="{0:.4f}".format(QI.draw_down(ts),4)
        ret['sharpe']="{0:.4f}".format(QI.sharpe(ts),4)
        return ret

    def record_pnl(self):
        pnl = self.value()
        self.pnl_as_of_date.append((Data_API.Pricing_Database.pricing_date,pnl))

