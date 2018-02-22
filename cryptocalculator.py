import abc

import pandas as pd
import sqlite3
from datetime import datetime
from cryptoqueries import fetch_daily_btc_closing_prices


class CryptoCalculator(object, metaclass=abc.ABCMeta):
    
    def __init__(self):
        """ Queries the AV API for data which is stored in a pandas DataFrame. """
        self.df = fetch_daily_btc_closing_prices()
    
    @abc.abstractmethod
    def calculate_weekly_averages(self):
        pass
    
    @abc.abstractmethod
    def output_weekly_averages(self):
        """ Stores weekly averages to csv file. """
        pass
    
    @abc.abstractmethod
    def greatest_rel_span(self):
        pass
    
    @abc.abstractmethod
    def store_data(self):
        pass


class PersistenceCalculator(CryptoCalculator):
    """ Uses SQLAlchemy to persist the DataFrame to a sqlite db. """

    def __init__(self):
        super(PersistenceCalculator, self).__init__()
        
        # handle db connection
        self.conn = sqlite3.connect(':memory:')
        self.df.to_sql('data', self.conn, index=True, if_exists='replace')
        
    def calculate_weekly_averages(self):
        rows_list = []
    
        c = self.conn.cursor()
        c.execute('Select * from data')
    
        all_rows = c.fetchall()
    
        week_sum = 0
        days_in_week = 1
        date_str = ''
        for row in all_rows:
            date = datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S')

            week_sum += row[1]
            if date.weekday() == 0:
                if days_in_week == 1:
                    continue
                date_str = date.strftime('%Y-%m-%d')
                rows_list.append({'date': date_str, 'average': (week_sum / days_in_week)})
            
                week_sum = 0
                days_in_week = 0
            days_in_week += 1
        if week_sum != 0:
            rows_list.append({'date': date_str, 'average': (week_sum / days_in_week - 1)})
    
        return pd.DataFrame(rows_list)
    
    def output_weekly_averages(self):
        weekly_avg = self.calculate_weekly_averages()
        weekly_avg.to_csv('out-indb.csv')
    
    def greatest_rel_span(self):
        return None
    
    def store_data(self):
        """ Stores to sqlite db. """
        pass
    
    def __enter__(self):
        self.conn = sqlite3.connect('sqlite:///crypto.db')
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()


class InMemoryCalculator(CryptoCalculator):
    output_file = 'data.csv'
    
    def calculate_weekly_averages(self):
        weekly_avg = self.df.groupby(pd.Grouper(freq='W-MON')).mean()
        weekly_avg = weekly_avg.rename(columns={'close': 'weekly average'})
        return weekly_avg
        
    def output_weekly_averages(self):
        weekly_avg = self.calculate_weekly_averages()
        weekly_avg.to_csv('out-inmem.csv')
    
    def greatest_rel_span(self):
        return None
    
    def store_data(self):
        """ Stores to CSV file. """
        pass


mem = InMemoryCalculator()
per = PersistenceCalculator()

print(mem.output_weekly_averages())
print(per.output_weekly_averages())

