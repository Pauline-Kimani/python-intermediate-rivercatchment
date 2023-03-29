"""Module containing models representing catchment data.

The Model layer is responsible for the 'business logic' part of the software.

Catchment data is held in a Pandas dataframe (2D array) where each column contains
data for a single measurement site, and each row represents a single measurement
time across all sites.
"""

import pandas as pd
import numpy as np


def with_logging(func):
    """"A decorator which adds logging to a function."""
    def inner(*args, **kwargs):
        print("Before function call")
        result = func (*args, **kwargs)
        print("After function call")
        return result

@with_logging
def add_two(n):
    print("Adding two")
    return n + 2
print(add_one(1))
print(add_two(1))

# def add_one(n):
    # print("Adding one")
    # return n + 1
# def add_two(x):
    # return add_one(add_one(x))

# using decorators to measure time taken to perform a function
import time

def profile(func):
   def inner(*args, **kwargs):
       start = time.process_time_ns()
       result = func(*args, **kwargs)
       stop = time.process_time_ns()

       print("Took {0} seconds".format((stop - start) / 1e9))
       return result

   return inner

@profile
def measure_me(n):
   total = 0
   for i in range(n):
       total += i * i

   return total

print(measure_me(1000000))

def data_above_threshold(site_id, data, threshold):
    return list(map(lambda x: x > threshold, data[site_id]))

    # noinspection PyUnreachableCode
    def count_above_threshold(a,b):
        if b:
            return a +1
        else:
            return a
    above_threshold = map(lambda x: x > threshold, data[site_id])
    return reduce(count_above_threshold, above_threshold, 0)

# using reduce
from functools import reduce
seq = [1, 2, 3, 4, 5]
def sum(a, b):
    return a + b
print(reduce(sum, seq))


def data_normalise(data):
    max_array = np.array(np.max(data, axis=0))
    return data / max_array[np.newaxis, :]


def read_variable_from_csv(filename):
    """Reads a named variable from a CSV file, and returns a
    pandas dataframe containing that variable. The CSV file must contain
    a column of dates, a column of site ID's, and (one or more) columns
    of data - only one of which will be read.

    :param filename: Filename of CSV to load
    :return: 2D array of given variable. Index will be dates,
             Columns will be the individual sites
    """
    dataset = pd.read_csv(filename, usecols=['Date', 'Site', 'Rainfall (mm)'])

    dataset = dataset.rename({'Date': 'OldDate'}, axis='columns')
    dataset['Date'] = [pd.to_datetime(x, dayfirst=True) for x in dataset['OldDate']]
    dataset = dataset.drop('OldDate', axis='columns')

    new_dataset = pd.DataFrame(index=dataset['Date'].unique())

    for site in dataset['Site'].unique():
        new_dataset[site] = dataset[dataset['Site'] == site].set_index('Date')["Rainfall (mm)"]

    new_dataset = new_dataset.sort_index()

    return new_dataset

def daily_total(data):
    """Calculate the daily total of a 2D data array.

        :param data: A 2D Pandas data frame with measurement data.
                     Index must be np.datetime64 compatible format. Columns are measurement sites.
        :returns: A 2D Pandas data frame with total values of the measurements for each day.
        """
    return data.groupby(data.index.date).sum()

def daily_mean(data):
    """Calculate the daily mean of a 2D data array.

        :param data: A 2D Pandas data frame with measurement data.
                     Index must be np.datetime64 compatible format. Columns are measurement sites.
        :returns: A 2D Pandas data frame with total values of the measurements for each day.
        """
    return data.groupby(data.index.date).mean()


def daily_max(data):
    """Calculate the daily max of a 2D data array.

        :param data: A 2D Pandas data frame with measurement data.
                     Index must be np.datetime64 compatible format. Columns are measurement sites.
        :returns: A 2D Pandas data frame with total values of the measurements for each day.
        """
    return data.groupby(data.index.date).max()


def daily_min(data):
    """Calculate the daily min of a 2D data array.

        :param data: A 2D Pandas data frame with measurement data.
                     Index must be np.datetime64 compatible format. Columns are measurement sites.
        :returns: A 2D Pandas data frame with total values of the measurements for each day.
        """
    return data.groupby(data.index.date).min()

