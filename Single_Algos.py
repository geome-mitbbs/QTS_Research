algos = {
    "moving average": """portfolio.buy(ticker) if average(ticker,-25)<average(ticker,-10) else portfolio.sell(ticker)"""
}