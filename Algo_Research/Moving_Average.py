# an exhaustive research on moving average strategy
import sys
import os
this_dir=os.path.dirname(__file__)
sys.path.append(this_dir+"\..\\")

from Back_Test import *
from Ticker_API import *
from Data_API import *
from Util import *
import Single_Algos

# Test 1 ---------------------------------
#run moving average on all SP500 underlyers
cache = Cache()
#Cache.quandl_key = "Put your quandl key here if you want better download speed with Quandl"
sp500 = get_snp500()
sp500_by_sector = get_snp500_by_sector()

Pricing_Database.lazy_update_data = True # to use downloaded data in the past week.
count = 0
good_keys = []
for k in sp500:
    try:
        if k == "JEC":
            raise Exception('Unadjusted ticker')
        cache.get_ticker_data(k)
        count += 1
        good_keys.append(k)
    except:
        print( "skipped {}".format(k) )
        pass

all_measures = []
all_measures_by_sector = []
all_measures_total ={}
for sector in sp500_by_sector:
    sector_measures = {}
    sector_counter = 0
    for k in sp500_by_sector[sector]:
        if k in good_keys:
            print(k)
            algo = back_test_single(Single_Algos.algos["moving average"],-2500,-1,ticker=k)
            temp_measure = algo.portfolio.get_measures()
            sector_measures={ key:temp_measure[key]+sector_measures.get(key,0) for key in temp_measure}
            all_measures_total={ key:temp_measure[key]+all_measures_total.get(key,0) for key in temp_measure}
            temp_measure['ticker'] = k
            all_measures.append(temp_measure)
            sector_counter += 1
    sector_measures = {key:sector_measures[key]/sector_counter for key in sector_measures}
    sector_measures['ticker'] = sector
    all_measures_by_sector.append(sector_measures)
all_measures_total = {key:all_measures_total[key]/count for key in all_measures_total}
all_measures_total['ticker'] = "Avg_SP500"

list_for_csv = [all_measures_total]+all_measures_by_sector+all_measures
dict_array_to_csv(list_for_csv,"Moving_Average_Result.csv",fields=['ticker','return','volatility','draw_down','sharpe'])

# Test 2 ---------------------------------
#run moving average with short selling on all SP500 underlyers
cache = Cache()
#Cache.quandl_key = "Put your quandl key here if you want better download speed with Quandl"
sp500 = get_snp500()
sp500_by_sector = get_snp500_by_sector()

Pricing_Database.lazy_update_data = True # to use downloaded data in the past week.
count = 0
good_keys = []
for k in sp500:
    try:
        if k == "JEC":
            raise Exception('Unadjusted ticker')
        cache.get_ticker_data(k)
        count += 1
        good_keys.append(k)
    except:
        print( "skipped {}".format(k) )
        pass

all_measures = []
all_measures_by_sector = []
all_measures_total ={}
for sector in sp500_by_sector:
    sector_measures = {}
    sector_counter = 0
    for k in sp500_by_sector[sector]:
        if k in good_keys:
            print(k)
            algo = back_test_single(Single_Algos.algos["moving average with short sell"],-2500,-1,ticker=k)
            temp_measure = algo.portfolio.get_measures()
            sector_measures={ key:temp_measure[key]+sector_measures.get(key,0) for key in temp_measure}
            all_measures_total={ key:temp_measure[key]+all_measures_total.get(key,0) for key in temp_measure}
            temp_measure['ticker'] = k
            all_measures.append(temp_measure)
            sector_counter += 1
    sector_measures = {key:sector_measures[key]/sector_counter for key in sector_measures}
    sector_measures['ticker'] = sector
    all_measures_by_sector.append(sector_measures)
all_measures_total = {key:all_measures_total[key]/count for key in all_measures_total}
all_measures_total['ticker'] = "Avg_SP500"

list_for_csv = [all_measures_total]+all_measures_by_sector+all_measures
dict_array_to_csv(list_for_csv,"Moving_Average_With_Short_Sell_Result.csv",fields=['ticker','return','volatility','draw_down','sharpe'])
