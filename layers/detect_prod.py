
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
from flask import Flask,request
from flask_cors import CORS, cross_origin
from flask.ext.cors import CORS

from second_layer import SecondLayer

sys.path.insert(0, '../components/')

 
app = Flask(__name__)

app.config['CORS_HEADERS'] = 'Content-Type'
app.config['CORS_RESOURCES'] = {r"/*": {"origins": "*"}}

#cors = CORS(app, resources={r"/api/*": {"origins": "http://localhost:port"}},headers='Content-Type')
cors = CORS(app)

# Holds polling information for all URLs and sentiments ever. I'm so sorry.
global polling_data
polling_data = {}


@cross_origin(origin='*',allow_headers="*",send_wildcard='true')



@app.route('/update_polls_pos', methods=["POST"])
def update_dict_pos():
    global poll
    query = request.data
    print(query)
    link_name =(str(query)[1:-1])
    print("yes!")
    if polling_data[link_name] is None:
        polling_data[link_name] = [1, 0]
    else:
        polling_data[link_name][0] += 1
    return_results()

def return_results(url):
    return polling_data[url]

@app.route('/update_polls_neg', methods=["POST"])
def update_dict_neg():
    global poll
    query = request.data
    print(query)
    link_name = (str(query)[1:-1])
    if polling_data[link_name] is None:
        polling_data[link_name] = [0, 1]
    else:
        polling_data[link_name][1] += 1
    return_results

@app.route('/check_selected', methods=['POST'])
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





@app.after_request
def after_request(response):
  #response.headers.add('Access-Control-Allow-Origin', 'null')
  #response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  #response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
  response.headers.add('Access-Control-Allow-Credentials', 'true')
  return response

if __name__ == "__main__":
    app.run()

app.run()
