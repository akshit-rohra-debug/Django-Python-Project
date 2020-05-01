import pandas as pd
import imp
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer 
from sklearn.naive_bayes import MultinomialNB

def getStringArrayFromNumpyDataFrame(dataframe):
    list=[]
    for s in dataframe.values:
        if len(str(s[0]))>0:
            list.append(str(s[0]))
    return list

def getEmotions(text,clf,count_vect,tfidf_transformer):
	text=text.split()
	X_new_counts = count_vect.transform(text)
	X_new_tfidf = tfidf_transformer.transform(X_new_counts)
	predicted = clf.predict(X_new_tfidf)
	positive_count=0
	for x in predicted:
		if x==1:
			positive_count=positive_count+1
	return positive_count;

def getEmotionFromText(text,clf_positive,clf_negative,clf_bad,count_vect,tfidf_transformer):
	positives=getEmotions(text,clf_positive,count_vect,tfidf_transformer)
	negatives=getEmotions(text,clf_negative,count_vect,tfidf_transformer)
	bad=getEmotions(text,clf_bad,count_vect,tfidf_transformer)
	if(bad>0):
		return("Negative")
	else:
		if(positives-negatives)>0:
			return("Positive")
		elif(negatives-positives)>0:
			return("Negative")
		else:
			return("Neutral")

def createmodel(line):
	train_data_csv_name="trumpwords.csv"

	df_x_words = pd.read_csv(train_data_csv_name,usecols=[0],header=None)
	df_y_positive= pd.read_csv(train_data_csv_name,usecols=[1],header=None)
	df_y_negative= pd.read_csv(train_data_csv_name,usecols=[2],header=None)
	df_y_bad= pd.read_csv(train_data_csv_name,usecols=[3],header=None)

	count_vect = CountVectorizer()
	X_train_counts = count_vect.fit_transform(getStringArrayFromNumpyDataFrame(df_x_words))
	tfidf_transformer = TfidfTransformer()
	X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)

	clf_positive = MultinomialNB().fit(X_train_tfidf, df_y_positive.values.ravel())
	clf_negative = MultinomialNB().fit(X_train_tfidf, df_y_negative.values.ravel())
	clf_bad = MultinomialNB().fit(X_train_tfidf, df_y_bad.values.ravel())

	tmpstr=getEmotionFromText(line,clf_positive,clf_negative,clf_bad,count_vect,tfidf_transformer)
	return tmpstr

#print(createmodel(line))

