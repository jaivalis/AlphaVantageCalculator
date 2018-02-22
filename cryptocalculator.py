import abc


class CryptoCalculator(object, metaclass=abc.ABCMeta):
    
    def __init__(self):
        """ Queries the AV API for data which is stored in a pandas DataFrame. """
        self.df = []
    
    @abc.abstractmethod
    def get_weekly_average(self, start_date):
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
    
    def get_weekly_average(self):
        return None
    
    def day_high_low(self):
        return None
    
    def store_data(self):
        """ Stores to sqlite db. """
        pass


class InMemoryCalculator(CryptoCalculator):
    output_file = 'data.csv'
    
    def get_weekly_average(self):
        return None
    
    def day_high_low(self):
        return None
    
    def store_data(self):
        """ Stores to CSV file. """
        pass


mem = InMemoryCalculator()
per = PersistenceCalculator()

