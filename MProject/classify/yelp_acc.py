import imp
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score


def getStringArrayFromNumpyDataFrame(dataframe):
    l = []
    for s in dataframe.values:
        if len(str(s[0])) > 0:
            l.append(str(s[0]))
    return l


def getEmotions(text, clf, count_vect, tfidf_transformer):
    text = text.split()
    X_new_counts = count_vect.transform(text)
    X_new_tfidf = tfidf_transformer.transform(X_new_counts)

    predicted = clf.predict(X_new_tfidf)
    count = 0
    for x in predicted:
        if x == 1:
            count = count + 1
    return count;


def getEmotionFromText(text, clf_positive, clf_negative, count_vect, tfidf_transformer):
    positives = getEmotions(text, clf_positive, count_vect, tfidf_transformer)
    negatives = getEmotions(text, clf_negative, count_vect, tfidf_transformer)
    #	bad=getEmotions(text,clf_bad)
    #	if(bad>0):
    #		return 0
    #	else:
    if (positives - negatives) > 0:
        return 1
    elif (negatives - positives) > 0:
        return 0
    else:
        return 0


def itsmain():
    tweet_file_name = "yelp_data.csv"
    train_data_csv_name = "trumpwords.csv"

    df_x_words = pd.read_csv(train_data_csv_name, usecols=[0], header=None)
    df_y_positive = pd.read_csv(train_data_csv_name, usecols=[1], header=None)
    df_y_negative = pd.read_csv(train_data_csv_name, usecols=[2], header=None)
    # df_y_bad= pd.read_csv(train_data_csv_name,usecols=[3],header=None)

    count_vect = CountVectorizer()
    X_train_counts = count_vect.fit_transform(getStringArrayFromNumpyDataFrame(df_x_words))
    tfidf_transformer = TfidfTransformer()
    X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)

    clf_positive = MultinomialNB().fit(X_train_tfidf, df_y_positive.values.ravel())
    clf_negative = MultinomialNB().fit(X_train_tfidf, df_y_negative.values.ravel())
    # clf_bad = MultinomialNB().fit(X_train_tfidf, df_y_bad.values.ravel())

    data = pd.read_csv("yelp_result.csv", header=None)
    index = 0
    with open(tweet_file_name, encoding="utf-8", errors='ignore') as f:
        pred = []
        actual = []
        for line in f:
            try:
                tmp = getEmotionFromText(line, clf_positive, clf_negative, count_vect, tfidf_transformer)
                pred.append(tmp)
                x = int(data.iloc[index, 0])
                actual.append(x)
                index = index + 1
            except:
                pass

    cm = confusion_matrix(actual, pred)
    acc = accuracy_score(actual, pred) * 100
    return acc, cm
