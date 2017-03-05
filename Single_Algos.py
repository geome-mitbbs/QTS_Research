single_algos = {
    "moving average":
    """
if average(ticker,-25)<average(ticker,-10):
    portfolio.buy(ticker)
elif average(ticker,-25)>average(ticker,-10):
    portfolio.sell(ticker)
"""
}