import os
import pandas as pd
import alpaca_trade_api as tradeapi
from dotenv import load_dotenv
from MCForecastTools import MCSimulation

load_dotenv() 

class Monte_Carlo:
    ''' 
    A Python class to return Monte Carlo simulation data.
    
    '''
    
    def __init__(self, alpaca_key, alpaca_secret, stock_list, trading_interval, start_date, end_date, weights, simulations, num_trading_days):
        '''
    Constructs necessary attributes for Monte_Carlo object.
    
    Parameters
    ---------
    alpaca api key : string 
        called from env file
    alpaca secret key : string 
        called from env file
    stock_list : list
        stock tickers inputted by user, up to and including three different stocks
    trading_interval : string
        how long each interval is, defaulted to one day
    start_date : string
        formated as 'YYYY-MM-DD'
    end_date : string
        formated as 'YYYY-MM-DD'
    weights : list(float)
        portfolio investment breakdown
    simulations : int
        how many times the monte carlo program will run a calculation
    num_trading_days : int
        how long of a period the monte carlo program will project forward, default 252 trading days in a year
        '''
        
        self.alpaca_key = alpaca_key
        self.alpaca_secret = alpaca_secret
        self.stock_list = stock_list
        self.trading_interval = trading_interval
        self.start_date = start_date
        self.end_date = end_date
        self.weights = weights
        self.simulations = simulations
        self.num_trading_days = numtradingdays
        
    def make_dataframe(self):
        '''
        Constructs a Pandas DataFrame from api data pulled from Alpaca based on given user inputs
        Dropps all columns except for closing price, places the stock symbol above the columns as a key
        
        '''
        
        api = tradeapi.REST(
        self.alpaca_key,
        self.alpaca_secret,
        )

        #creates the dataframe
        df_tickers = api.get_bars(
            self.stock_list,
            self.trading_interval,
            start = pd.Timestamp(self.start_date, tz='America/New_York').isoformat(),
            end= pd.Timestamp(self.end_date, tz='America/New_York').isoformat(),
        ).df
                 
        df_tickers = df_tickers.drop(['open', 'high', 'low', 'volume', 'trade_count', 'vwap'], axis =1)

        if (len(self.stock_list) == 0):
            print ('Please enter stock ticker(s)')
        elif (len(self.stock_list) == 1):
            one = self.stock_list[0],
            df_tickers = pd.concat([one], axis =1, keys = [self.stock_list[0]])
        elif (len(tickers) ==2):
            one = self.stock_list[0]
            one = df_tickers[df_tickers["symbol"]==one].drop("symbol", axis=1)
            two = self.stock_list[1]
            two = df_tickers[df_tickers["symbol"]==two].drop("symbol", axis=1)
            df_tickers = pd.concat([one, two], axis =1, keys = [self.stock_list[0], self.stock_list[1]])
        elif (len(tickers) ==3):
            one = self.stock_list[0]
            one = df_tickers[df_tickers["symbol"]==one].drop("symbol", axis=1)
            two = self.stock_list[1]
            two = df_tickers[df_tickers["symbol"]==two].drop("symbol", axis=1)
            three = self.stock_list[2]
            three =df_tickers[df_tickers["symbol"]==three].drop("symbol", axis=1)
            df_tickers = pd.concat([one, two, three], axis =1, keys = [self.stock_list[0], self.stock_list[1], self.stock_list[2]])
        elif (len(self.stock_list) > 3):
              print('Overflow error, please select between one to three stock tickers.')
        
                
        self.df_tickers = df_tickers
        
            

        return df_tickers

    def forecast(self):
        '''
        Runs a Monte Carlo calculation based on user inputs.
        
        '''
        if len(self.stock_list) != len(self.weights):
            print('Error--Number of stocks and number of weights must match!')

        
        MC_even_dist = MCSimulation(
        portfolio_data = self.df_tickers,
        weights = self.weights,
        num_simulation = self.simulations,
        num_trading_days = self.num_trading_days
    )
        
        self.data = MC_even_dist
        self.cumulative_return = MC_even_dist.calc_cumulative_return()
        
        return self.data
    
    def make_line_plot(self):
        '''
        Returns a line plot projection of the previously run Monte Carlo simulation.
        
        '''
        
        if len(self.stock_list) != len(self.weights):
            print('Error--Number of stocks and number of weights must match!')
        
        line_graph = self.data.plot_simulation()
        return line_graph
    
    def make_bar_graph(self):
        '''
        Returns a histogram chart, plotting the probability distribution and confidence intervals. 
        
        '''
        
        if len(self.stock_list) != len(self.weights):
            print('Error--Number of stocks and number of weights must match!')
        
        bar_graph = self.data.plot_distribution()
        return bar_graph
    
    
    
    
    '''
        Quick tutorial:
        Enter the Parameters: 
        
        ..........................

        example = Monte_Carlo(
        alpaca_key = alpaca_api_key,
        alpaca secret = alpaca_secret_key,
        stock_list = tickers,
        trading_interval = timeframe,
        start_date = start,
        end_date = end,
        weights = weights,
        simulations = numSim,
        numTradingDays = NumTradingDays    
        )
        ..........................
        
        Commands to call the functions within the class:
        
        ..........................
        
        example.make_dataframe()
        example.forecast()
        example.make_line_plot()
        example.make_bar_graph()
        
        ..........................
    '''