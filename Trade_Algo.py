try:
    from . import Portfolio
    from . import Data_API
    from .Quant_Indicators import *
except:
    import Portfolio
    import Data_API
    from Quant_Indicators import *

class Trade_Algo:
    def __init__(self,command=None):
        self.command = command
        if not self.safety_check():
            self.command = """raise Exception("not safe to run")"""

    def filter_string(self):
        # first suppress all the """sss""" string.
        new_command = ""
        left_quotes_saw = 0
        left_quotes_pos = []
        for i in range(len(self.command)):
            if(self.command[i] != "\""):
                left_quotes_saw = 0
            else:
                if(left_quotes_saw<3):
                    left_quotes_saw += 1
                if(left_quotes_saw==3):
                    left_quotes_pos.append(i-2)
                    left_quotes_saw = 0

        if(len(left_quotes_pos)//2 * 2 != len(left_quotes_pos)):
            raise Exception("Not proper string")

        if(len(left_quotes_pos)==0):
            return self.command

        for i in range(len(left_quotes_pos)//2):
            if i==0:
                new_command += self.command[0:left_quotes_pos[2*i]]
            else:
                new_command += self.command[left_quotes_pos[2*i-1]+3:left_quotes_pos[2*i]]

            if i== len(left_quotes_pos)//2-1:
                new_command += self.command[left_quotes_pos[2*i+1]+3:]

        return new_command

    def find_used_vars(self):
        new_command = self.filter_string()
        ret = dict()
        list = ['portfolio','portfolio1','portfolio2','portfolio3','quant_index','quant_index1','quant_index2','quant_index3']
        for item in list:
            if item in new_command:
                ret[item] = None
        self.used_vars = ret

    def find_tickers(self):
        # find all the "ABC" in the command and they should be all the tickers
        if(self.command == """raise Exception("not safe to run")"""):
            self.tickers = []
            return

        new_command = self.filter_string()
        tickers = []
        current_ticker = ""
        saw_left_quote = False
        for c in new_command:
            if not saw_left_quote:
                if c != "\"":
                    pass
                else:
                    saw_left_quote = True
            else:
                if c != "\"":
                    current_ticker += c
                else:
                    tickers.append(current_ticker)
                    current_ticker = ""
                    saw_left_quote = False
        self.tickers = tickers

    def safety_check(self):
        # check if self.command is safe to run....need this before go production
        return True

    def back_test(self,start_date=None,end_date=None,initial_cash=0,initial_portfolio=None):
        if end_date == None:
            end_date = Data_API.Pricing_Database.pricing_date
        if isinstance(start_date,int):
            start_date = Data_API.add_pricing_date(start_date,in_place=False)
        if isinstance(end_date,int):
            end_date = Data_API.add_pricing_date(end_date,in_place=False)
        #for pnl
        if initial_portfolio == None:
            portfolio = Portfolio.Portfolio(initial_cash)
            portfolio1=Portfolio.Portfolio(initial_cash)
            portfolio2=Portfolio.Portfolio(initial_cash)
            portfolio3=Portfolio.Portfolio(initial_cash)
        else:
            portfolio = initial_portfolio
            portfolio1 = initial_portfolio
            portfolio2 = initial_portfolio
            portfolio3 = initial_portfolio

        #for information
        quant_index=[]
        quant_index1=[]
        quant_index2=[]
        quant_index3=[]
        self.find_tickers()
        self.find_used_vars()
        cache = Data_API.Cache()
        for ticker in self.tickers:
            cache.get_ticker_data(ticker)
        #set back the date.
        orig_pd = Data_API.Pricing_Database.pricing_date
        try:
            Data_API.set_pricing_date(start_date)
            while Data_API.Pricing_Database.pricing_date <= end_date:
                exec(self.command)
                portfolio.record_pnl()
                portfolio1.record_pnl()
                portfolio2.record_pnl()
                portfolio3.record_pnl()
                Data_API.add_pricing_date(1)
            self.portfolio = portfolio
            self.portfolio1 = portfolio1
            self.portfolio2 = portfolio2
            self.portfolio3 = portfolio3
            self.quant_index = quant_index
            self.quant_index1=quant_index1
            self.quant_index2=quant_index2
            self.quant_index3=quant_index3
            Data_API.set_pricing_date(orig_pd)

            self.pnls = {'portfolio':self.portfolio.pnl_as_of_date,\
            'portfolio1':self.portfolio1.pnl_as_of_date,\
            'portfolio2':self.portfolio2.pnl_as_of_date,\
            'portfolio3':self.portfolio3.pnl_as_of_date}
            self.quant_indices = {'quant_index':self.quant_index,\
                                  'quant_index1':self.quant_index1,\
                                  'quant_index2':self.quant_index2,\
                                  'quant_index3':self.quant_index3}
        except Exception as e:
            Data_API.set_pricing_date(orig_pd)
            raise e

    def back_test_summary(self):
        output = ""
        if "portfolio" in self.used_vars:
            output += """portfolio:\n""" + str(self.portfolio.get_measures()) + """\n"""
        if "portfolio1" in self.used_vars:
            output += """portfolio1:\n""" + str(self.portfolio1.get_measures()) + """\n"""
        if "portfolio2" in self.used_vars:
            output += """portfolio2:\n""" + str(self.portfolio2.get_measures()) + """\n"""
        if "portfolio3" in self.used_vars:
            output += """portfolio3:\n""" + str(self.portfolio3.get_measures()) + """\n"""

        return output

    def back_test_plot(self):
        import matplotlib.pyplot as plt
        import matplotlib.dates as mdates
        fig = plt.figure()
        all_lines = []
        ax = fig.add_subplot(111)
        ax.set_ylabel('PnL')
        has_right_ax = False
        if 'quant_index' in self.used_vars or \
            'quant_index1' in self.used_vars or \
            'quant_index2' in self.used_vars or \
            'quant_index3' in self.used_vars:
            has_right_ax = True
        dates = [ x[0] for x in self.pnls['portfolio'] ]
        for v in self.used_vars:
            if 'portfolio' in v:
                all_lines += ax.plot(dates, [x[1] for x in self.pnls[v]],label=v,linewidth=1)

        if has_right_ax:
            right_ax = ax.twinx()
            for v in self.used_vars:
                if 'index' in v:
                    all_lines += right_ax.plot(dates, self.quant_indices[v],label=v,linewidth=1,ls='dotted')
            
            right_ax.set_ylabel('quant_index')

        # format the ticks
        years = mdates.YearLocator()   # every year
        months = mdates.MonthLocator()  # every month
        yearsFmt = mdates.DateFormatter('%Y')

        ax.xaxis.set_major_locator(years)
        ax.xaxis.set_major_formatter(yearsFmt)
        ax.xaxis.set_minor_locator(months)
        datemin = min(dates)
        datemax = max(dates)
        ax.set_xlim(datemin, datemax)
        ax.format_xdata = mdates.DateFormatter('%Y-%m-%d')
        ax.grid(True)


        # rotates and right aligns the x labels, and moves the bottom of the
        # axes up to make room for them
        fig.autofmt_xdate()
        fig.tight_layout()
        plt.legend(all_lines,[l.get_label() for l in all_lines],loc='best')
        plt.show()        
