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

df = concatenated_df.groupby(['SCHOOL', 'MAJOR_CODE_1', 'ADMIT_TERM', 'TERM_CODE'])['UNIQUE_ID'].nunique()

print(df)

all_admit_terms = concatenated_df.drop_duplicates(subset=['ADMIT_TERM'], inplace = False)
all_admit_terms.sort_values(['ADMIT_TERM'], ascending=True, inplace=True)

admit_terms = []

i = 1
for admit_term in all_admit_terms['ADMIT_TERM']:
    admit_terms.append([admit_term, i])
    i = i+1

admit_terms= pd.DataFrame(admit_terms)

df = pd.DataFrame(df)

df.join(admit_terms)

print(df)
'''
concatenated_df.drop_duplicates(subset=['UNIQUE_ID','TERM_CODE'], inplace = True)
number_of_majors = concatenated_df.groupby(['MAJOR_CODE_1', 'ADMIT_TERM', 'TERM_CODE'])['MAJOR_CODE_1'].count() #Gets number of students majoring in each

#Convert new attributes to pandas dataframes
number_of_majors = number_of_majors.to_frame()
number_of_credits = number_of_credits.to_frame()

number_of_majors.columns = ['NUM_STUDENTS']

#Concatenate new dataframes
frames = [number_of_majors, number_of_credits]

result = pd.concat(frames, axis=1, join='inner')
result = result.reset_index()

print(result)

for i in range(len(result)):
    new_value = result.loc[i, 'CREDITS_ATTEMPTED'] / result.loc[i, 'NUM_STUDENTS']
    result.set_value(i, 'CREDITS_ATTEMPTED', new_value)

result = result.rename(columns={'CREDITS_ATTEMPTED': 'CREDITS_ATTEMPTED_PER_STUDENT', 'MAJOR_CODE_1': 'MAJOR'})

#result = result.set_index(['MAJOR'])

df1 = result.loc[result.MAJOR=='CHEM']
df1['CREDITS_ATTEMPTED_PER_STUDENT'].plot(figsize=(15, 6))
plt.ylabel('Credits Per Student for CHEM')
plt.show()
'''
