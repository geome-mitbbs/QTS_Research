from Trade_Algo import *
import sys

if len(sys.argv) > 1:
    file_name = sys.argv[1]
    with open(file_name, 'r') as myfile:
        data=myfile.read()
    t = Trade_Algo(data)
else:
    #example: moving average strategy. 
    algo_msg = """
ticker = "MSFT"
if average(ticker,-25)<average(ticker,-10):
    portfolio.buy(ticker)
elif average(ticker,-25)>average(ticker,-10):
    portfolio.sell(ticker)
quant_index.append(average(ticker,-25)/average(ticker,-10))
"""
    print("No user strategy specified. To specify a strategy, write it into a txt file \
and append as the first argument of the command")
    print("Run the example strategy below" )
    print( algo_msg )
    t = Trade_Algo(algo_msg)

t.back_test(-250,-1,initial_cash=1000000)
print(t.back_test_summary())
t.back_test_plot()
