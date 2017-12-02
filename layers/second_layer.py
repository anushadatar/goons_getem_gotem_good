#!/usr/bin/env python
# -*- coding: utf-8 -*-
from textblob import TextBlob
from textblob.classifiers import NaiveBayesClassifier
import grammar_check

from newspaper import Article
import newspaper
import requests
import dateutil
from bs4 import BeautifulSoup
import requests
import csv
import numpy
import urllib
import wikipedia



# TODO List
# Implement clickbaity headline analyzer
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

input_text = '''Hip Hop star Jay Z has blasted traditional Christian values in an epic rant where he claims to be part of an exclusive club of “Smart people” who worships “our true lord; Satan.”  The billionaire rapper has also claimed that “God created Lucifer to be the bearer of truth and light, and that “Jesus never existed” but was merely a “tool created by smart people to control dumb people.” During a backstage tirade at the Smoothie King Center in New Orleans on Friday, Jay Z pointed around the room saying, Ya’ll are being played.'''

class second_layer():
    """
    A news article. Should ideally have raw text input.
    """
    def __init__(self, input_text, url):
        self.url = url
        self.raw_text = input_text.decode('utf-8')
        self.head = input_text[0:self.raw_text.find("\n")]
        self.headline = self.head.decode('utf-8')
        self.text = TextBlob(self.raw_text)
        self.polarity = self.text.sentiment[0]
        self.subjectivity = self.text.sentiment[1]
        self.sentiment_metric = self.compute_sentiment_metric()
        self.grammar_metric = self.compute_grammar_metric()
        self.title_metric = self.compute_clickbait_metric()
        self.author_info = self.find_author()
        self.websites, self.category = self.parse_suspicious_websites()
        self.TLD_score = self.check_TLD()
        self.domain_score = self.check_domain()
        self.author_score = self. check_author()

    def compute_sentiment_metric(self):
        """
        Turns string of article text body into a sentiment percentage. The higher
        the overall polairty (positive/negative bias) or
        """
        return ((abs(self.polarity) + self.subjectivity)/2)*100

    def compute_grammar_metric(self):
        """
        Computes grammar metric for text set.
        """
        tool = grammar_check.LanguageTool('en-US')
        matches = tool.check(self.raw_text)
        approximate_number_of_words = self.raw_text.count(" ") + 1
        metric =((approximate_number_of_words- len(matches))/float(approximate_number_of_words))
        return (metric * 100)

    def compute_clickbait_metric(self):
        """
        Computes clickbaityness metric for text set.
        """
        train = [
            ("Whoa Trump Orders Congress to Go After Deep State Obama Holdovers", "neg"),
            ("Marked for ‘De-escalation Syrian Towns Endure Surge of Attacks", "pos")
        ]
        cl = NaiveBayesClassifier(train)
        if classify(self.headline) == "pos":
            return 100
        else:
            return 0

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

    def parse_suspicious_websites(self):
        websites = []
        category = []
        with open('sources.csv', 'r', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for row in reader:
                websites.append(row[0])
                if row[1] == "bias":
                    category.append(2)
                elif row[1] == "clickbait":
                    category.append(1)
                elif row[1] == "conspiracy":
                    category.append(3)
                elif row[1] == "unreliable":
                    category.append(4)
                elif row[1] == "fake":
                    category.append(7)
                elif row[1] == "political":
                    category.append(1)
                elif row[1] == "rumor":
                    category.append(3)
                elif row[1] == "junksci":
                    category.append(3)
                elif row[1] == "hate":
                    category.append(4)
        return websites, category

    def check_TLD(self):
        url_split_1 = self.url.split('/')
        suspicious_TLD = [".country", ".stream", ".gdn", ".mom", ".xin", ".kim",
                            ".men", ".loan", ".download", ".racing", ".online",
                            ".science", ".ren", ".gb", ".win", ".top", ".review",
                            ".vip", ".party", ".tech", ".co.com", ".wordpress"]
        safe_TLD = [".com", ".org", ".edu", ".co", ".gov"]

        for i in range(len(suspicious_TLD)):
            if url_split_1[2].find(suspicious_TLD[i]) != -1:
                trusted_domain = 4
                break
        if trusted_domain < 1:
            for i in range(len(safe_TLD)):
                if url_split_1[2].find(safe_TLD[i]) != -1:
                    trusted_domain = 0;
                    break
        return trusted_domain

    def check_domain(self):
        for i in range(len(self.websites)):
            if (url_split_1[2]).find(self.websites[i]) != -1:
                suspicious_site = category[i]
                break
        return suspicious_site

    def check_author(self):
        for message in self.author_info.split("\n"):
            if (message != "No Authors Found") and (message.find("substantial") == -1):
                return 0
            return 4


def test():
    input_text = "Hip Hop star Jay-Z has blasted traditional Christian values \n an epic rant where he claims to be part of an exclusive club of “Smart people” who worships “our true lord; Satan.” The billionaire rapper has also claimed that “God created Lucifer to be the bearer of truth and light, and that “Jesus never existed” but was merely a “tool created by smart people to control dumb people.”During a backstage tirade at the Smoothie King Center in New Orleans on Friday, Jay Z pointed around the room saying, “Ya’ll are being played.”"
    print("Running")
    test = second_layer(input_text)
    print(vars(test))

test()
