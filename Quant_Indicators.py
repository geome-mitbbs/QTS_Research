import numpy as np
import inspect
import sys
import pydoc

try:
    from . import Data_API
except:
    import Data_API
    
def smart_index(obj,iter_index,default=None):
    if(iter_index<0 or iter_index >= len(obj)):
        return default
    else:
        return obj[iter_index]
    
def time_index(time_index_array,dt=None):
    if dt == None:
        dt = Data_API.Pricing_Database.pricing_date
    index = np.searchsorted(time_index_array,dt)
    if(index==len(time_index_array)):
        return len(time_index_array)-1
    elif time_index_array[index] == dt:
        return index
    else:
        return index - 1

def is_biz_day(ticker,dt=None):
    if dt==None:
        dt = Data_API.Pricing_Database.pricing_date
    cache = Data_API.Cache()
    dates = cache.get_ticker_dates(ticker)
    index = time_index(dates,dt)
    if(dates[index] == dt):
        return True
    else:
        return False

def price(ticker,date_offset=-1,price_feature='Close'):
    """
    ticker: the underlyer ticker to price of
    date_offset: int, default to -1, -k means the k-th last day as of observation
    price_feature: default to 'Close', can use 'Open', 'Close', 'High', 'Low'
    """
    cache = Data_API.Cache()
    data = cache.get_ticker_data(ticker)
    pricing_date_index = time_index(data.index.values)
    if(date_offset<0):
        date_offset = date_offset+1+pricing_date_index
    elif date_offset>pricing_date_index:
        date_offset = pricing_date_index
    return data[price_feature][date_offset]

def prices(ticker,start=0,end=-1,price_feature='Close'):
    cache = Data_API.Cache()
    data = cache.get_ticker_data(ticker)
    pricing_date_index = time_index(data.index.values)
    if(start<0):
        start = start+1+pricing_date_index
    elif start>pricing_date_index:
        start = pricing_date_index
    if(end<0):
        end = end+1+pricing_date_index
    elif end>pricing_date_index:
        end = pricing_date_index
    return np.array(data[price_feature][start:end+1])

def price_return(obj, start=0, end=-1,price_feature='Close'):
    """
    obj: the underlyer ticker to price of. Or it can be an numpy array
    start: int, default to 0, -k means the k-th last day as of observation
    end: int, default to -1, -k means the k-th last day as of observation
    price_feature: default to 'Close', can use 'Open', 'Close', 'High', 'Low'
    """
    if(isinstance(obj,str)):
        obj = prices(obj,start,end,price_feature)
        start = 0
        end = -1
    return obj[end]/obj[start] - 1.0

def log_price_return(obj, start=0, end=-1,price_feature='Close'):
    """
    obj: the underlyer ticker to price of. Or it can be an numpy array
    start: int, default to 0, -k means the k-th last day as of observation
    end: int, default to -1, -k means the k-th last day as of observation
    price_feature: default to 'Close', can use 'Open', 'Close', 'High', 'Low'
    """
    if(isinstance(obj,str)):
        obj = prices(obj,start,end,price_feature)
        start = 0
        end = -1
    return np.log(obj[end]/obj[start])

def price_returns(obj, start=0, end=-1,price_feature='Close',step=1):
    """
    obj: the underlyer ticker to price of. Or it can be an numpy array
    start: int, default to 0, -k means the k-th last day as of observation
    end: int, default to -1, -k means the k-th last day as of observation
    price_feature: default to 'Close', can use 'Open', 'Close', 'High', 'Low'
    """
    if(isinstance(obj,str)):
        obj = prices(obj,start,end,price_feature)
        start = 0
        end = -1

    if(end<0):
        end += len(obj)

    start_step = start + step
    rets = np.array([obj[idx]/obj[idx-step]-1.0 for idx in range(start_step,end+1)])
    return rets

def log_price_returns(obj, start=0, end=-1,price_feature='Close',step=1):
    """
    obj: the underlyer ticker to price of. Or it can be an numpy array
    start: int, default to 0, -k means the k-th last day as of observation
    end: int, default to -1, -k means the k-th last day as of observation
    price_feature: default to 'Close', can use 'Open', 'Close', 'High', 'Low'
    """
    if(isinstance(obj,str)):
        obj = prices(obj,start,end,price_feature)
        start = 0
        end = -1

    if(end<0):
        end += len(obj)

    start_step = start + step
    rets = np.log(np.array([obj[idx]/obj[idx-step] for idx in range(start_step,end+1)]))
    return rets

def volatility(obj, start=0, end=-1,price_feature='Close'):
    """
    obj: the underlyer ticker to price of. Or it can be an numpy array
    start: int, default to 0, -k means the k-th last day as of observation
    end: int, default to -1, -k means the k-th last day as of observation
    price_feature: default to 'Close', can use 'Open', 'Close', 'High', 'Low'
    """
    if(isinstance(obj,str)):
        obj = prices(obj,start,end,price_feature)
        start = 0
        end = -1
    if end == -1:
        # end = -1 is a corner case here since (end+1) will be 0
        end = len(obj) - 1
    daily_change = np.log(obj[start+1:end+1]/obj[start:end])
    std = np.std(daily_change)
    vol = np.sqrt(Data_API.Pricing_Database.trading_days) * std
    return vol

def max_draw_down(obj, start=0, end=-1, price_feature='Close'):
    if isinstance(obj,str):
        obj = prices(obj,start,end,price_feature)
        start = 0
        end = -1

    if end == -1:
        # end = -1 is a corner case here since (end+1) will be 0
        end = len(obj) - 1

    draw_downs = []
    current_max = None
    for i in range(start,end+1):
        if current_max == None:
            current_max = obj[i]+0.0
        elif obj[i]>current_max:
            current_max = obj[i]+0.0
        draw_downs.append((obj[i]-current_max)/current_max)

    max_d = np.min(draw_downs)
    return min([0.0,max_d])

def draw_down(obj, start=0, end=-1, price_feature='Close'):
    """
    obj: the underlyer ticker to price of. Or it can be an numpy array
    start: int, default to 0, -k means the k-th last day as of observation
    end: int, default to -1, -k means the k-th last day as of observation
    price_feature: default to 'Close', can use 'Open', 'Close', 'High', 'Low'
    """
    if(isinstance(obj,str)):
        obj = prices(obj,start,end,price_feature)
        start = 0
        end = -1

    if end == -1:
        # end = -1 is a corner case here since (end+1) will be 0
        end = len(obj) - 1

    min_price = np.min(obj[start:end+1])
    return min([0.0,(min_price - obj[start]) / obj[start]])

def sharpe(obj, start=0, end=-1,price_feature='Close'):
    """
    obj: the underlyer ticker to price of. Or it can be an numpy array
    start: int, default to 0, -k means the k-th last day as of observation
    end: int, default to -1, -k means the k-th last day as of observation
    price_feature: default to 'Close', can use 'Open', 'Close', 'High', 'Low'
    """
    if(isinstance(obj,str)):
        obj = prices(obj,start,end,price_feature)
        start = 0
        end = -1

    if end <0:
        end += len(obj)

    ndays = end - start + 1
    annual_return = (1 + price_return(obj,start,end)) ** (float(Data_API.Pricing_Database.trading_days) / ndays) - 1
    vol = volatility(obj,start,end)
    if annual_return == 0:
        return 0
    return annual_return / vol

def all_indicators_doc():
    all_funcs = inspect.getmembers(sys.modules[__name__], inspect.isfunction)
    ret = ""
    for f in all_funcs:
        ret += pydoc.render_doc(f[1], renderer = pydoc.plaintext).splitlines()[2] + "\n"
    return ret

def average(obj, start=0, end=-1, price_feature='Close'):
    if isinstance(obj, str):
        obj = prices(obj, start, end, price_feature)
        start = 0
        end = -1

    if end < 0:
        end += len(obj)
    if start < 0:
        start += len(obj)

    return np.mean(obj[start: (end + 1)])


def max(obj, start=0, end=-1, price_feature='Close'):
    if isinstance(obj, str):
        obj = prices(obj, start, end, price_feature)
        start = 0
        end = -1

    if end < 0:
        end += len(obj)
    if start < 0:
        start += len(obj)

    return np.max(obj[start: (end + 1)])


def min(obj, start=0, end=-1, price_feature='Close'):
    if isinstance(obj, str):
        obj = prices(obj, start, end, price_feature)
        start = 0
        end = -1

    if end < 0:
        end += len(obj)
    if start < 0:
        start += len(obj)

    return np.min(obj[start: (end + 1)])

def rsi(obj, start=-14, end=-1, price_feature='Close'):
    if isinstance(obj, str):
        obj = prices(obj, start, end, price_feature)
        start = 0
        end = -1

    if end < 0:
        end += len(obj)
    if start < 0:
        start += len(obj)

    _data = np.diff(obj[start: (end + 1)])
    len_gain = len(_data[_data > 0.0])
    len_loss = len(_data[_data < 0.0])
    if len_gain == 0 or len_loss == 0:
        return 50
    average_gain = np.mean(_data[_data > 0.0])
    average_loss = np.abs(np.mean(_data[_data < 0.0]))
    first_rs = average_gain / average_loss
    rsi = 100 - 100 / (1 + first_rs)

    return rsi

def correlation(obj1, obj2, start=0, end=-1, price_feature='Close'):
    if isinstance(obj1, str) or isinstance(obj2, str):
        obj1 = log_price_returns(obj1, start, end, price_feature)
        obj2 = log_price_returns(obj2, start, end, price_feature)
        # simple and rough treatment: assume biz days are the same among the two tickers
        if len(obj1)>len(obj2):
            obj1 = obj1[len(obj1)-len(obj2):]
        else:
            obj2 = obj2[len(obj2)-len(obj1):]
        start = 0
        end = -1

    if end < 0:
        end += len(obj1)
    if start < 0:
        start += len(obj1)

    return np.corrcoef(obj1[start: (end + 1)], obj2[start: (end + 1)])[0, 1]

