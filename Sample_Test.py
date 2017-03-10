from Back_Test import *
import Single_Algos

algo_str ="""
portfolio.buy(ticker) if average(ticker,-10)>average(ticker,-25) else portfolio.sell(ticker)
if(average(ticker,-10)>average(ticker,-25) and price(ticker)>average(ticker,-200)):
    portfolio1.buy(ticker)
elif(average(ticker,-10)<average(ticker,-25) and price(ticker)<average(ticker,-200)):
    portfolio1.sell(ticker)
portfolio2.buy(ticker)
"""
#quant_index.append(price(ticker))

t = back_test_single(algo_str,-2500,-1,ticker="AAPL")
print(t.back_test_summary())
t.back_test_plot()
