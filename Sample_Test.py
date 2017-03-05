from Back_Test import *
algo_str = """portfolio.buy("AAPL") if average("AAPL",-25)<average("AAPL",-10) else portfolio.sell("AAPL")"""
t = back_test_single(algo_str,-2500,-1)
print(t.back_test_summary())
t.back_test_plot()
