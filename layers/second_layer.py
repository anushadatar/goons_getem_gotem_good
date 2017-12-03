#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sumy.parsers.html import HtmlParser
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer as Summarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words

#from google import google
#import goolge


from textblob import TextBlob
from textblob.classifiers import NaiveBayesClassifier
#import grammar_check

#from newspaper import Article
#import newspaper
import requests
import dateutil
from bs4 import BeautifulSoup
import requests
import csv
import numpy
import urllib
import wikipedia
import json
from flask import jsonify




# TODO List
# Fix clickbait analyzer
# Give that a lot more training data`
# Impletment pandas series to plain text conversion
# Worry about python 2 and 3 library conflicts
# Think about how to hand data over the UI
# Build the entire UI and also the web framework (oh yeah, that)
# Implement alternate article lookup

# TODO Figure out how this compiles into JS for the extensions
# TODO Figure out how to best hand this over to the UI
# TODO Add
# TODO Add text summarization feature
    # Then, add suggestions feature

class SecondLayer():
    """
    A news article. Should ideally have raw text input.
    """
    def __init__(self, input_text, url, rating):
        self.rating = rating
        self.url = url
        self.raw_text = input_text.encode('utf-8', 'ignore').decode('utf-8')
        self.head = input_text[0:self.raw_text.find("\n")]
        self.headline = self.head.encode('utf-8', 'ignore').decode('utf-8')
        self.text = TextBlob(self.raw_text)
        self.polarity = self.text.sentiment[0]
        self.subjectivity = self.text.sentiment[1]
        self.sentiment_metric = self.compute_sentiment_metric()
        #self.grammar_metric = self.compute_grammar_metric()
        #self.title_metric = self.compute_clickbait_metric()
        self.grammar_metric = 0
        self.title_metric = 0
        #self.author_info = self.find_author()
        self.author_info = 0
        self.websites, self.category = self.parse_suspicious_websites()
        self.TLD_score = self.check_TLD()
        self.domain_score = self.check_domain()
        #self.author_score = self. check_author()
        self.total_score = self.compute_total_score()

    def compute_sentiment_metric(self):
        """
        Turns string of article text body into a sentiment percentage. The higher
        the overall polairty (positive/negative bias) or
        """
        return (((2 * abs(self.polarity) - 1) + (2 * self.subjectivity) - 1) / 2) * 10

    def compute_grammar_metric(self):
        """
        Computes grammar metric for text set.
        """
        tool = grammar_check.LanguageTool('en-US')
        matches = tool.check(self.raw_text)
        approximate_number_of_words = self.raw_text.count(" ") + 1
        metric =((approximate_number_of_words- len(matches))/float(approximate_number_of_words))
        return (((2 * metric) - 1) * 10)

    def compute_clickbait_metric(self):
        """
        Computes clickbaityness metric for text set.
        """
        train = [
            ("Whoa Trump Orders Congress to Go After Deep State Obama Holdovers", "neg"),
            ("Marked for ‘De-escalation Syrian Towns Endure Surge of Attacks", "pos"),
            ("Perfume E-Mail Raises a Stink.", "neg"),
            ("Woman Pricked by Hidden Needle", "neg"),
            ("Four Accused in Facebook Live Torture Case Plead Not Guilty.", "neg"),
            ("Mayor Tries to Save Warren Buffett's Old Berkshire Hathaway Headquarters", "pos"),
            ("Senate Passes Sweeping Republican Tax Overhaul Bill", "pos"),
            ("Colombian General Captured, Released by Rebels Resigns", "pos"),
            ("Bulldog Bites Pedophile’s Penis Off as He Tried to Rape Sleeping Children.", "neg"),
            ("The Scallop Sees With Space-Age Eyes — Hundreds of Them", "pos")
        ]

        for i in range(10):
            temp = (train[i][0], train[i][1])
            temp = (train[i][0].decode('utf-8'), train[i][1])
            train[i] = temp

        cl = NaiveBayesClassifier(train)
        blob = TextBlob(self.head, classifier = cl)
        if blob.classify() == "pos":
        if classify(self.headline) == "pos":
            return 15
        else:
            return 0

    '''
    def find_author(self):
        a = Article(self.url)
        a.download()
        a.parse()
        authors = a.authors
        message = "No Authors Found"
        if authors != None:
            message = ""
            for author in authors:
                message += find_author_wiki(self, author) + "\n"
        return message

    def find_author_wiki(self, author):
        message = "No substantial information about " + author + " found"
        author_names = author.split(" ")
        if wikipedia.search(author) == None:
            return message
        else:
            if len(wikipedia.search(author)) < 5:
                searches = len(wikipedia.search(author))
            else:
                searches = 5
            for result in wikipedia.search(author):
                content = wikipedia.page(result).content
                if (content.find(author_names[0]) != -1) and (content.find(author_names[-1]) != -1):
                    return wikipedia.page(result).summary
                return message
    '''
    def parse_suspicious_websites(self):
        websites = []
        category = []
        with open('sources.csv', 'r') as csvfile:
            self.reader = csv.reader(csvfile, delimiter=',')
            for row in self.reader:
                websites.append(row[0])
                if row[1] == "bias":
                    category.append(5)
                elif row[1] == "clickbait":
                    category.append(10)
                elif row[1] == "conspiracy":
                    category.append(10)
                elif row[1] == "unreliable":
                    category.append(10)
                elif row[1] == "fake":
                    category.append(15)
                elif row[1] == "political":
                    category.append(15)
                elif row[1] == "rumor":
                    category.append(10)
                elif row[1] == "junksci":
                    category.append(5)
                elif row[1] == "hate":
                    category.append(10)
            return websites, category

    def check_TLD(self):
        self.url_split_1 = self.url.split('/')
        suspicious_TLD = [".country", ".stream", ".gdn", ".mom", ".xin", ".kim",
                            ".men", ".loan", ".download", ".racing", ".online",
                            ".science", ".ren", ".gb", ".win", ".top", ".review",
                            ".vip", ".party", ".tech", ".co.com", ".wordpress"]
        safe_TLD = [".com", ".org", ".edu", ".co", ".gov"]
        trusted_domain = 5
        for i in range(len(suspicious_TLD)):
            if self.url_split_1[2].find(suspicious_TLD[i]) != -1:
                trusted_domain = 30
                break
        if trusted_domain < 30:
            for i in range(len(safe_TLD)):
                if self.url_split_1[2].find(safe_TLD[i]) != -1:
                    trusted_domain = -5;
                    break
        return trusted_domain

    def check_domain(self):
        suspicious_site = 0
        for i in range(len(self.websites)):
            if (self.url_split_1[2]).find(self.websites[i]) != -1:
                suspicious_site = self.category[i]
                break
        return suspicious_site
    """
    def check_author(self):
        for message in self.author_info.split("\n"):
            if (message != "No Authors Found") and (message.find("substantial") == -1):
                return 0
            return 4
    """

    def compute_total_score(self):
        final_score = 0
        if self.rating == "REAL":
            final_score = 25
        else:
            final_score = 75
        final_score += self.TLD_score + self.domain_score + self.grammar_metric + self.sentiment_metric + self.title_metric
        if final_score > 99:
            final_score = 99
        if final_score < 1:
            final_score = 1
        return ((final_score * 2) - 100) / 100

    def json(self):

        results = {'final_score': self.total_score,
                'sentiment_metric': self.sentiment_metric,
                'title_metric': self.title_metric,
                'grammar_metric': self.grammar_metric,
                'domain_score': self.domain_score,
                'TLD_score': self.TLD_score,
                'initial_rating': self.rating}


        result = json.dumps(results)
        loaded_results = jsonify(result)
        # loaded_results['results'] #Output 3.5
        # type(results) #Output str
        #  type(loaded_results) #Output dict
        return loaded_results


def test():
    input_text = "Hip Hop star Jay-Z has blasted traditional Christian values \n an epic rant where he claims to be part of an exclusive club of “Smart people” who worships “our true lord; Satan.” The billionaire rapper has also claimed that “God created Lucifer to be the bearer of truth and light, and that “Jesus never existed” but was merely a “tool created by smart people to control dumb people.”During a backstage tirade at the Smoothie King Center in New Orleans on Friday, Jay Z pointed around the room saying, “Ya’ll are being played.”"
    url = "http://www.breitbart.com/big-government/2017/12/01/michael-flynn-report-trump-white-house-caught-off-guard-flynn-plea-counsel-didnt-know/"
    rating = "FAKE"
    print("Running")
    test = SecondLayer(input_text, url, rating)
    print(test.json())

#test()
