'''
    Program to analyze data using ARIMA model
    Output plots of forecasts
'''

import warnings
import itertools
import pandas as pd
import numpy as np
from statsmodels.tsa.arima_model import ARIMA
from sklearn.metrics import mean_squared_error
from math import sqrt
import os
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')

#Load data
CleanedData = pd.read_csv('CleanedData.csv', index_col=0, low_memory=False, parse_dates=['DATE']) #Change term code column to date time when possible

#Get list of majors
majors = CleanedData['MAJOR'].unique().tolist()

#Loop through all majors
for major in majors:
    df1 = CleanedData.loc[CleanedData.MAJOR==major]
    df1 = df1.convert_objects(convert_numeric=True)
    data = df1.ix[1:]   #Drops first row of data (can't derive change in credits with no previous data)

    #Only analyze data if there are at least 5 data points
    if(len(data)>=5):
        directory = '/home/chris/Desktop/ProjectingMajorGrowth/FordhamAnalyticsInternship/Plots/' + major
        if not os.path.exists(directory):
            os.makedirs(directory)

        #Plot data
        data['CHANGE_IN_CREDITS_ATTEMPTED'].plot(figsize=(15, 6))
        plt.ylabel('Change in Credits for ' + major)
        plt.savefig(directory + '/' + major + '_data.png')
        plt.close()

        #Define the p, d and q parameters to take any value between 0 and 2
        p = d = q = range(0, 2)

        #Generate all different combinations of p, q and q triplets
        pdq = list(itertools.product(p, d, q))
        print(pdq)

        warnings.filterwarnings("ignore") #Specify to ignore warning messages

        start = len(data)//2
        end = len(data)
        resultlist = []

        #Optimize pdq parameters using AIC
        for param in pdq:
            try:
                mod = ARIMA(data['CHANGE_IN_CREDITS_ATTEMPTED'], order=param)

                results = mod.fit(disp=0)
                resultlist.append(results.aic)

                print('ARIMA{} - AIC:{}'.format(param, results.aic))
            except:
                continue

        try:
            index = resultlist.index(min(resultlist))
            final_pdq = pdq[index]
            print(final_pdq)

            mod = ARIMA(data['CHANGE_IN_CREDITS_ATTEMPTED'], order=final_pdq)

            results = mod.fit(disp=0)

            print(results.summary().tables[1])

            #Plot forecasts against actual data
            results.plot_predict(start=start, end=end+5, dynamic=True, plot_insample=True)
            plt.savefig(directory + '/' + major + '_projection.png')
            plt.close()

        except:
            pass
