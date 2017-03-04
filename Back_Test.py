from Trade_Algo import *

t = Trade_Algo("""
ticker = "AAPL"
if average(ticker,-25)<average(ticker,-10):
    portfolio.buy(ticker)
elif average(ticker,-25)>average(ticker,-10):
    portfolio.sell(ticker)
""")
t.back_test(-250,-1,initial_cash=1000000)
print(t.back_test_summary())
