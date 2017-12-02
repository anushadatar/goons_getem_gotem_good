
from __future__ import print_function

import logging
import pandas as pd
import numpy as np
from optparse import OptionParser
import sys
import ast
from time import time
import matplotlib.pyplot as plt

from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.feature_selection import SelectFromModel
from sklearn.feature_selection import SelectKBest, chi2
from sklearn.linear_model import RidgeClassifier
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.utils.extmath import density
from sklearn import metrics

from bs4 import BeautifulSoup as Soup
from textblob import TextBlob
from goose import Goose
from requests import get

url = ""
if sys.argv[1]:
	url = sys.argv[1]
else:
	print("Error: Website URL not specified.")
	exit()

response = get(url)
extractor = Goose()
article = extractor.extract(raw_html=response.content)
text = article.cleaned_text

ds = pd.Series([text])

filename1 = "fake_or_real_news.csv"
data1 = pd.read_csv(filename1)

headlines_train = data1.title
articles_train = data1.text
states_train = data1.label

articles_test = ds

k_store = 500

feature_names = None

vectorizer = HashingVectorizer(stop_words='english', strip_accents='unicode', alternate_sign=False, n_features=500)
ch2 = SelectKBest(chi2, k=k_store)
X_train = vectorizer.fit_transform(articles_train)
X_test = vectorizer.transform(articles_test)
Y_train = states_train
X_train = ch2.fit_transform(X_train, Y_train)

if feature_names:
	feature_names = [feature_names[i] for i in ch2.get_support(indices=True)]

if feature_names:
    feature_names = np.asarray(feature_names)

clf = LinearSVC(penalty="l1", dual=False, tol=1e-3)
clf.fit(X_train, Y_train)
pred = clf.predict(X_test)

print(pred[0])

