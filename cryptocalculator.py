import abc

import pandas as pd

from cryptoqueries import fetch_daily_btc_closing_prices


class CryptoCalculator(object, metaclass=abc.ABCMeta):
    
    def __init__(self):
        """ Queries the AV API for data which is stored in a pandas DataFrame. """
        self.df = fetch_daily_btc_closing_prices()
        print(self.df)
    
    @abc.abstractmethod
    def output_weekly_averages(self):
        """ Stores weekly averages to csv file. """
        pass
    
    @abc.abstractmethod
    def day_high_low(self):
        pass
    
    @abc.abstractmethod
    def store_data(self):
        pass
    
    def relative_span(self, date):
        high, low = self.day_high_low(date)
        
        if low == 0:
            return 0
        return (high - low) / low


class PersistenceCalculator(CryptoCalculator):
    """ Uses SQLAlchemy to persist the DataFrame to a sqlite db. """

    def __init__(self):
        super(PersistenceCalculator, self).__init__()
        
        # handle db connection.
    
    def output_weekly_averages(self):
        return None
    
    def day_high_low(self):
        return None
    
    def store_data(self):
        """ Stores to sqlite db. """
        pass


class InMemoryCalculator(CryptoCalculator):
    output_file = 'data.csv'
    
    def output_weekly_averages(self):
        self.df.index = pd.to_datetime(self.df.index, format='%Y-%m-%d')
        weekly_avg = self.df.groupby(pd.Grouper(freq='W-MON')).mean()
        weekly_avg = weekly_avg.rename(columns={'close': 'weekly average'})
        weekly_avg.to_csv('out.csv')
    
    def day_high_low(self):
        return None
    
    def store_data(self):
        """ Stores to CSV file. """
        pass


mem = InMemoryCalculator()
per = PersistenceCalculator()

print(mem.output_weekly_averages())

