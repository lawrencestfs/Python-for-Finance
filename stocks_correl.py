##!/usr/bin/python
# -*- coding: utf-8 -*-

# File Name: stocks_correl.py
# Author: Lawrence Fernandes
# Copyright (C) 2016 Lawrence Fernandes

""" This module reads csv files containing stocks historical prices and calculates 
its Pearson's correlation coefficient over their returns. It also creates a correlation matrix graphic.
The csv files must be taken from Yahoo Finance and must contain the same date interval.
"""
# Import Python standard modules
import glob
import sys
from time import clock, sleep, localtime, strftime
# Import external modules
import pandas as pd
import scipy.stats
import numpy
import matplotlib.pyplot as plt

# Global variables
path = "C:\\Users\\Antonio\\Documents\\Lawrence\\BCC\\Práticas de Pesquisa\\IBrX 100\\*.csv"
cvs_stocks = glob.glob(path) # Using glob to get the path
stock_returns = [] # Stores the daily returns of all stocks

def read_files():
    """ Reads csv files containing historical prices and calculates the daily returns of the stocks """
    i = 0
    l = len(cvs_stocks)
    print("\nReading stocks data: \n")
    # Initial call to print 0% progress
    print_progress(i, l, prefix = 'Progress:', suffix = 'Complete', barLength = 50)
    for stock in cvs_stocks:
        df = pd.read_csv(stock)
        # Reads the Close column of the csv file
        close_column = df.Close

        #columns = ['Adj Close']
        #close_column = pd.DataFrame(df, columns=columns)
        
        # Daily_return = close_price - previous_day_close_price
        # Enumerate with conditional inside the list comprehension:
        daily_returns = [x - close_column[i - 1] for i, x in enumerate(close_column) if i > 0]
        # Add the daily returns of a stock to the list of stock returns
        stock_returns.append(daily_returns)
        sleep(0.1)
        # Update Progress Bar
        i += 1
        print_progress(i, l, prefix = 'Progress:', suffix = 'Complete', barLength = 50)

def compute_correlation():
    """ Calculates the Pearson correlation between the stocks and saves it to a txt file """
    i = 0
    l = len(cvs_stocks)
    print("\nCalculating stocks correlations: \n")
    print_progress(i, l, prefix = 'Progress:', suffix = 'Complete', barLength = 50)
    f = open("dataset.txt", "w+")
    f.write("%d %d" % (len(stock_returns),2))
    for i in range(len(stock_returns)):
        for j in range(i + 1, len(stock_returns)):
            # Using SciPy to calculate Pearson's correlation coefficient:
            correl = scipy.stats.pearsonr(stock_returns[i], stock_returns[j])#[0]
            f.write("%d %d %s\n" % (i,j,correl))
        sleep(0.1)
        i += 1
        print_progress(i, l, prefix = 'Progress:', suffix = 'Complete', barLength = 50)
    f.close()

def correlation_matrix():
    """ Creates a correlation matrix of the stocks read """
    # Using NumPy to calculate Pearson's correlation coefficient:
    correlation_matrix = numpy.corrcoef(stock_returns)
    # Using matplotlib to draw the correlation matrix
    plt.imshow(correlation_matrix,interpolation='nearest')
    plt.colorbar()
    plt.show()

def print_progress (iteration, total, prefix = '', suffix = '', decimals = 1, barLength = 100):
    """ Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        barLength   - Optional  : character length of bar (Int)
    """
    formatStr       = "{0:." + str(decimals) + "f}"
    percents        = formatStr.format(100 * (iteration / float(total)))
    filledLength    = int(round(barLength * iteration / float(total)))
    bar             = '█' * filledLength + '-' * (barLength - filledLength)
    sys.stdout.write('\r%s |%s| %s%s %s' % (prefix, bar, percents, '%', suffix)),
    if iteration == total:
        sys.stdout.write('\n')
    sys.stdout.flush()

def menu():
    """ Creates an options menu """
    print('\nUsage: %s [-option]' % sys.argv[0])
    print('where the options are the following:')
    print('  -c    Reads csv files containing historical stock prices and calculates their correlation coefficient.')
    print('  -m    Draws a correlation matrix of the stocks read using matplotlib.')

def main():
    print('\nStarting csv_reader at %s' % strftime("%Y-%m-%d %H:%M:%S", localtime()))
    print('(c) 2016 Lawrence Fernandes')
    option = ' '.join(sys.argv[1:])
    Done = False
    while not Done:
        if option not in {'-c','-m'}:
                print("\nInvalid option! Please, try again.")
                menu()
                break
        else:
            if option=="-c":
                start_time = clock()
                read_files()
                compute_correlation()
                elapsed = clock()-start_time
                print("\n--- Task done in %.2f seconds ---" % (elapsed))
                break
            elif option=="-m":
                start_time = clock()
                read_files()
                correlation_matrix()
                elapsed = clock()-start_time
                print("\n--- Task done in %.2f seconds ---" % (elapsed))
                break

if __name__ == '__main__':
    main()
