#!/usr/bin/env python
from __future__ import print_function

import logging
import pandas as pd
import numpy as np
from optparse import OptionParser
import sys
import ast
from time import time
import matplotlib.pyplot as plt
import json

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
from requests import *
# from flask import Flask,request
# from flask_cors import CORS, cross_origin
# from flask.ext.cors import CORS

from second_layer import SecondLayer

sys.path.insert(0, '../components/')


"""
This is a test file for working on the interface between the first and 
second layer without the external issues of flask and with the possibility
of custom input. To make it work, copy the csv files necessary into
this layers directory. 

"""


 
def check_selected():
    global selected
    query = request.data
    print(query)
    return (classifyURL(str(query)[1:-1]))

def classifyURL(url):
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
	second = SecondLayer(text, url,  pred[0])
	data = second.json()
	print(data)
	return data	

def after_request(response):
  #response.headers.add('Access-Control-Allow-Origin', 'null')
  #response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  #response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
  response.headers.add('Access-Control-Allow-Credentials', 'true')
  return response

if __name__ == "__main__":
    classifyURL("http://www.cnn.com/2017/12/02/opinions/foreign-service-will-survive-with-or-without-tillerson-kirby-opinion/index.html")
