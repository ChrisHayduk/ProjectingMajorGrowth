'''
Program to retrieve Twitter data using CIP Code Labels.
Program takes very long to execute (Took several hours when tested with data Tweets going back to 06/14/2017).
May not be viable for multiple years of data
'''

import got3, pandas

excel = pandas.read_excel('CIP Codes Labels.xlsx', header=None)
labels = excel.get_values()

tweets = []

for label in labels:
    label = str(label[0])
    print(label)
    tweetCriteria = got3.manager.TweetCriteria().setQuerySearch(label).setSince("2017-06-14")
    tweets.append(got3.manager.TweetManager.getTweets(tweetCriteria))

print(len(tweets))

for i in range(len(tweets)):
    print(labels[i], ": ", len(tweets[i]))
