import twitter
import json
import csv
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS

	
csv_file = 'C:\\Users\\Daniel.Beach\\AppData\\Local\\Programs\\Python\\Python35-32\\tweets.csv'
key_file = 'C:\\Users\\Daniel.Beach\\AppData\\Local\\Programs\\Python\\Python35-32\\keys.json'

def loadSuperSecretKeys(key_file):
	file = key_file
	with open(file, 'r') as f:
		superSecrets = json.load(f)
	return superSecrets

def loadTwit(superSecrets):
	api = twitter.Api(consumer_key = superSecrets["consumer_key"],
		consumer_secret = superSecrets["consumer_secret"],
		access_token_key = superSecrets["access_token_key"],
		access_token_secret = superSecrets["access_token_secret"])
	return api
	
def searchTwit(api): #get tweets from past 7 days. You get what you pay for -> nothing.
	search = api.GetSearch("GitHub")
	for tweet in search:
		yield {tweet.id : tweet.text.encode('utf-8')}
		print(tweet.id)
		
def saveTwits(dict,csv_file,list):
	with open(csv_file, 'a', encoding='utf8') as csv:
		for k,v in dict.items():
			if k not in list:
				csv.write('"' + str(k) + '","' + str(v).replace(',','') + '"\n')
			
def readTwitIDs(csv_file):
	idList = []
	df = pd.read_csv(csv_file)
	for column in df.iterrows():
		idList.append(column[1][0])
	return idList

def analyzeTwits(csv_file):
	text = ''
	df = pd.read_csv(csv_file)
	for column in df.iterrows():                                                                            
		text = text + ' ' + str(column[1][1])
	return text.replace('.','').replace(',','').replace('#','').replace('"','').replace('@','').replace('!','').replace(':','').replace('?','').replace("b'rt",' ').replace(' to ','').replace(' a ' ,' ').replace(' and ','').replace(' as ','').replace(' you ','').replace(' for ','')
	
def countWords(text):
	wordCounts = {}
	text = text.lower()
	words = text.split()
	for word in words:
		if word in wordCounts:
			wordCounts[word] += 1
		else:
			wordCounts[word] = 1
	frame = pd.DataFrame(list(wordCounts.items()),columns=['word','count'])
	frame = frame.sort('count', ascending=False).head(15)
	print(frame)
	stopwords = set(STOPWORDS)
	wordcloud = WordCloud(
                          background_color='white',
						  stopwords=stopwords,
                          max_words=10,
                          max_font_size=40, 
                          random_state=42
                         ).generate(str(frame['word']))

	print(wordcloud)
	fig = plt.figure(1)
	plt.imshow(wordcloud)
	plt.axis('off')
	plt.show()
	
def main():
		idList = readTwitIDs(csv_file)
		superSecrets = loadSuperSecretKeys(key_file)
		api = loadTwit(superSecrets)
		tweeties = searchTwit(api)
		for t in tweeties:
			saveTwits(t,csv_file,idList)
		text = analyzeTwits(csv_file)
		countWords(text)

if __name__ == '__main__': #<-allows import of file in other projects without executing code.
	main()