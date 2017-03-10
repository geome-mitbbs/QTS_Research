algos = {
    "moving average": """portfolio.buy(ticker) if average(ticker,-25)<average(ticker,-10) else portfolio.sell(ticker)""",
    "moving average with short sell":\
"""
portfolio.allow_short_sell=True
portfolio.flat(ticker)
if portfolio.current_portfolio['cash'] > 1.0:
    portfolio.buy(ticker,value=portfolio.current_portfolio['cash']-0.1) if average(ticker,-25)<average(ticker,-10) else portfolio.sell(ticker,value=portfolio.current_portfolio['cash']-0.1)
""",
    "moving average with support price":\
"""
portfolio.allow_short_sell=False
if(average(ticker,-10)>average(ticker,-25) and price(ticker)>average(ticker,-200)):
    portfolio.buy(ticker)
elif(average(ticker,-10)<average(ticker,-25) and price(ticker)<average(ticker,-200)):
    portfolio.sell(ticker)
"""
}