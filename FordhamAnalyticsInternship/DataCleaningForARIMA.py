'''
    Program to format data for use with ARIMA model
    Returns data grouped by major and term. Data includes number of students majoring in subject and change in number of credits taken
'''

import pandas as pd
import glob
import os

#Create path to data files
path = r'/home/chris/Desktop/ProjectingMajorGrowth/FordhamAnalyticsInternship/RegistrationDatawithEncryptedID-20Years'
all_files = glob.glob(os.path.join(path, "*.csv"))

#Load and aggregate data files
df_from_each_file = (pd.read_csv(f, low_memory=False) for f in all_files)
concatenated_df = pd.concat(df_from_each_file, ignore_index=True)

#Derive attributes to assist in data analysis
number_of_credits = concatenated_df.groupby(['MAJOR_CODE_1', 'TERM_CODE'])['CREDITS_ATTEMPTED'].sum() #Gets number of credits taken for each major

concatenated_df.drop_duplicates(subset=['UNIQUE_ID','TERM_CODE'], inplace = True)
number_of_majors = concatenated_df.groupby(['MAJOR_CODE_1', 'TERM_CODE'])['MAJOR_CODE_1'].count() #Gets number of students majoring in each

#Convert new attributes to pandas dataframes
number_of_majors = number_of_majors.to_frame()
number_of_credits = number_of_credits.to_frame()

number_of_majors.columns = ['NUM_STUDENTS']

#Concatenate new dataframes
frames = [number_of_majors, number_of_credits]

result = pd.concat(frames, axis=1, join='inner')
result = result.reset_index()
result['TERM_CODE'] = result['TERM_CODE'].astype('str')

print(result)
#Loop to change TERM_CODE to dates
i = 0
for x in result['TERM_CODE']:
    num_str = str(x)
    year = num_str[0:4]
    term = num_str[4:6]
    month = '5'
    day = '15'

    if term == '10':
        year = int(year)
        year = str(year-1)
        month = '12'


    date = year + '-' + month + '-' + day
    result.set_value(i, 'TERM_CODE', date)

    i=i+1

#Change TERM_CODE column to datetime values
result['TERM_CODE'] = pd.to_datetime(result['TERM_CODE'])
result = result.rename(columns={'TERM_CODE': 'DATE', 'CREDITS_ATTEMPTED': 'CHANGE_IN_CREDITS_ATTEMPTED', 'MAJOR_CODE_1': 'MAJOR'})

print(result)

majors = result['MAJOR'].unique().tolist()

#Changing number of credits to change in credits
#Not functional at the moment
x=0
for major in majors:
    x=x+1
    data = result.loc[result.MAJOR==major]
    for i in range(1, len(data)):
        new_value = data.iloc[i, 3] - data.iloc[i-1, 3]
        result.set_value(x, 'CHANGE_IN_CREDITS_ATTEMPTED', new_value)
        x = x+1

result = result.set_index(['DATE'])

#Output aggregated attributes to CSV
result.to_csv('CleanedData.csv')
