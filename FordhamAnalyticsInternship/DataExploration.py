'''
    Program to explore data
    Main purpose is to check behavior of cohorts (ie. Freshmen, Sophomores, etc.)
'''

import pandas as pd
import glob
import os
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')

#Create path to data files
path = r'/home/chris/Desktop/ProjectingMajorGrowth/FordhamAnalyticsInternship/RegistrationDatawithEncryptedID-20Years'
all_files = glob.glob(os.path.join(path, "*.csv"))

#Load and aggregate data files
df_from_each_file = (pd.read_csv(f, low_memory=False) for f in all_files)
concatenated_df = pd.concat(df_from_each_file, ignore_index=True)
