from Trade_Algo import *

#example: moving average strategy. 
t = Trade_Algo("""
ticker = "MSFT"
if average(ticker,-25)<average(ticker,-10):
    portfolio.buy(ticker)
elif average(ticker,-25)>average(ticker,-10):
    portfolio.sell(ticker)
quant_index.append(average(ticker,-25)/average(ticker,-10))
""")
t.back_test(-250,-1,initial_cash=1000000)
print(t.back_test_summary())
t.back_test_plot()
