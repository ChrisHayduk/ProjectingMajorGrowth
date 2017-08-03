'''
    Program to explore data
    Main purpose is to check behavior of cohorts (ie. Freshmen, Sophomores, etc.)
'''

import pandas as pd
import glob
import os
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')

#Load grouped data
data = pd.read_excel('Fall1997toSummer2017withGroupings.xlsx')

print(data)
