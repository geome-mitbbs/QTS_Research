from Data_API import *
from Trade_Algo import *
import random

def back_test_single(algo_str,start_date,end_date,ticker=None,ticker_list=[],random_ticker=False,random_start=False,random_end=False,initial_cash=1000000):
    """
    this tests single ticker strategies.
    ticker variable in the algo_str can be assigned value. hard-coded tickers in the algo_str will stay the same.
    This can randomize the ticker in the algo and also the testing time period.
    Randomization can reduce the bias.
    :return: backtested Algo
    """
    if random_ticker:
        ticker = random.choice(ticker_list)

    if ticker != None:
        full_algo_str = """ticker=\"{}\"""".format(ticker) + "\n" + algo_str
    else:
        full_algo_str = algo_str
    algo = Trade_Algo(full_algo_str)

    full_time_period = date_diff(start_date,end_date)

    if random_start:
        start_date = add_date(start_date,random.randint(0, full_time_period))

    if random_end:
        end_date = add_date(end_date,-random.randint(0, full_time_period))

    if random_start and random_end and end_date < start_date :
        start_date_copy = start_date
        start_date = end_date
        end_date = start_date_copy

    algo.back_test(start_date,end_date,initial_cash=initial_cash)
    return algo


