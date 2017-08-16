'''
    Program to make predictions using survival analysis
    Program currently loops through every major and asks user to input number of students in that school
'''

import pandas as pd
import glob
import os
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')

directory = '/home/chris/Desktop/ProjectingMajorGrowth/FordhamAnalyticsInternship/Plots/SurvivalAnalysis'

#Load grouped data
data = pd.read_excel('Fall1997toSummer2017withGroupings-Major1Only.xlsx')

termsList = data.ADMIT_TERM.unique()

for i in range(len(termsList)):
    termsList[i] = float(termsList[i])

termsList.sort()

termsList = termsList[:-1]

list = []

for i in range(len(termsList)):
    list.append((termsList[i], i+1))

print(list)

df = pd.DataFrame(list, columns = ["ADMIT_TERM", "START_TERM"])

temp = pd.merge(data, df, how='inner', on='ADMIT_TERM')

df2 = pd.DataFrame(list, columns = ["TERM_CODE", "END_TERM"])

result = pd.merge(temp, df2, how='inner', on='TERM_CODE')

differenceOfTerms = []

for i in range(len(result)):
    diff = result.iloc[i,10]-result.iloc[i,9]+1
    differenceOfTerms.append(diff)

se = pd.Series(differenceOfTerms)

result['RELATIVE_TERM'] = se.values

result.to_csv('DataWithRelativeTerms.csv')

schools = result['SCHOOL'].unique().tolist()

majors = result['MAJOR_CODE_1'].unique().tolist()

for school in schools:
    df1 = result.loc[result.SCHOOL==school]
    majors = df1['MAJOR_LABEL_1'].unique().tolist()

    for major in majors:
        max = df1['RELATIVE_TERM'].max()

        listOfProportions = [0] * max

        totalStudents = [0] * max

        for i in range(1, max+1):
            studentsInTerm = 0
            studentsInMajor = 0

            for j in range(len(df1)):
                if df1.iloc[j,11] == i:
                    studentsInTerm = studentsInTerm+1
                    if df1.iloc[j, 7] == major:
                        major_code = df1.iloc[j, 6]
                        studentsInMajor = studentsInMajor+1

            if studentsInTerm != 0:
                listOfProportions[i-1] = studentsInMajor/studentsInTerm
            totalStudents[i-1] = studentsInTerm

#Commented out this section of the code because the graphs have already been created
'''
        final_directory = directory + '/' + major_code + '/'

        if not os.path.exists(final_directory):
            os.makedirs(final_directory)

        plt.plot(listOfProportions)
        plt.ylabel('Proportion for ' + major)
        plt.xlabel('Relative Term')
        plt.savefig(final_directory + major_code + '_data.png')
        plt.close()
'''
        input_str = "Enter number of students in each relative term (ie. first term, second term, etc.) for school ", school, " separated by spaces: "
        rawInput = input(input_str)
        userInput = rawInput.split(' ')
        if userInput[0] == '':
            del userInput[0]

        sum = 0

        for x in range(len(userInput)):
            sum = sum + (listOfProportions[x]*float(userInput[x]))

        print("The predicted number of students majoring in ", major, " in school ", school, " is: ", sum, '\n')
