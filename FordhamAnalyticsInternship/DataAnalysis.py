import pandas as pd, sklearn, numpy, matplotlib.pyplot as plt, statsmodels

CleanedData = pd.read_csv('CleanedData.csv', index_col=2, low_memory=False) #Change term code column to date time when possible
del CleanedData['Unnamed: 0']

majors = CleanedData['MAJOR_CODE_1'].unique().tolist()

data = CleanedData.loc[CleanedData.MAJOR_CODE_1==majors[0]] #Test with one major

data.plot(figsize=(15, 6))
plt.show()

#Commented out code to loop through all majors
'''
for major in majors:
    data = CleanedData.loc[CleanedData.MAJOR_CODE_1==major]
'''
