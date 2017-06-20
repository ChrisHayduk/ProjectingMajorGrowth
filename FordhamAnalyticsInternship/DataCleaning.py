import pandas as pd
import glob
import os

#Create path to data files
path = r'/home/chris/Desktop/FordhamAnalyticsInternship/RegistrationDatawithEncryptedID-20Years'
all_files = glob.glob(os.path.join(path, "*.csv"))

#Load and aggregate data files
df_from_each_file = (pd.read_csv(f, low_memory=False) for f in all_files)

concatenated_df = pd.concat(df_from_each_file, ignore_index=True)

#Derive attributes to assist in data analysis
number_of_majors = concatenated_df.groupby(['MAJOR_CODE_1', 'TERM_CODE'])['MAJOR_CODE_1'].count() #Gets number of students majoring in each
number_of_credits = concatenated_df.groupby(['MAJOR_CODE_1', 'TERM_CODE'])['CREDITS_ATTEMPTED'].sum() #Gets number of credits taken for each major

#Convert new attributes to pandas dataframes
number_of_majors = number_of_majors.to_frame()
number_of_credits = number_of_credits.to_frame()

number_of_majors.columns = ['NUM_STUDENTS']

#Concatenate new dataframes
frames = [number_of_majors, number_of_credits]

result = pd.concat(frames, axis=1, join='inner')

#Output aggregated attributes to CSV
result.to_csv('CleanedData.csv')
