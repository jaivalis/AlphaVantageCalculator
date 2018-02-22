import abc
import sqlite3
import sys
from datetime import datetime

import pandas as pd

from cryptoqueries import fetch_daily_btc_closing_prices


class CryptoCalculator(object, metaclass=abc.ABCMeta):
    
    def __init__(self):
        """ Queries the AV API for data which is stored in a pandas DataFrame. """
        self.df = fetch_daily_btc_closing_prices()
    
    @abc.abstractmethod
    def calculate_weekly_averages(self):
        pass
    
    def output_weekly_averages(self, fname):
        weekly_avg = self.calculate_weekly_averages()
        weekly_avg.to_csv(fname + '.csv')
    
    @abc.abstractmethod
    def greatest_rel_span(self):
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
    
        week_sum = 0
        days_in_week = 1
        date_str = ''
        for row in c.fetchall():
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
            rows_list.append({'date': date_str, 'average': week_sum / (days_in_week-1)})
    
        return pd.DataFrame(rows_list)
    
    def greatest_rel_span(self):
        date_ret = ''
        c = self.conn.cursor()
        c.execute('Select * from data')
        
        max_rel_span = 0
        week_min = sys.maxsize
        week_max = 0
        for row in c.fetchall():
            date = datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S')
    
            week_min = min(week_min, row[1])
            week_max = max(week_max, row[1])
            if date.weekday() == 0:
                rel_span = (week_max - week_min) / week_min
                
                max_rel_span = max(max_rel_span, rel_span)
                if max_rel_span == rel_span:
                    date_ret = date.strftime('%Y-%m-%d')
                week_min = sys.maxsize
                week_max = 0
        return date_ret
        

class InMemoryCalculator(CryptoCalculator):
    output_file = 'data.csv'
    
    def calculate_weekly_averages(self):
        weekly_avg = self.df.groupby(pd.Grouper(freq='W-MON')).mean()
        weekly_avg = weekly_avg.rename(columns={'close': 'weekly average'})
        return weekly_avg

    def greatest_rel_span(self):
        weekly_min = self.df.groupby(pd.Grouper(freq='W-MON')).min()
        weekly_max = self.df.groupby(pd.Grouper(freq='W-MON')).max()
    
        relative_spans = (weekly_max - weekly_min) / weekly_min
        return relative_spans['close'].idxmax()
    
    
mem = InMemoryCalculator()
per = PersistenceCalculator()

mem.output_weekly_averages('inmem')
per.output_weekly_averages('fromdb')

print(mem.greatest_rel_span())
print(per.greatest_rel_span())
