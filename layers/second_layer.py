#!/usr/bin/env python
# -*- coding: utf-8 -*-
from textblob import TextBlob
from textblob.classifiers import NaiveBayesClassifier
import grammar_check


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
    def __init__(self, input_text):
        self.raw_text = input_text.decode('utf-8')
        self.head = input_text[0:self.raw_text.find("\n")]
        self.headline = self.head.decode('utf-8')
        self.text = TextBlob(self.raw_text)
        self.polarity = self.text.sentiment[0]
        self.subjectivity = self.text.sentiment[1]
        self.sentiment_metric = self.compute_sentiment_metric()
        self.grammar_metric = self.compute_grammar_metric()
        self.title_metric = self.compute_clickbait_metric()
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


def test():
    input_text = "Hip Hop star Jay-Z has blasted traditional Christian values \n an epic rant where he claims to be part of an exclusive club of “Smart people” who worships “our true lord; Satan.” The billionaire rapper has also claimed that “God created Lucifer to be the bearer of truth and light, and that “Jesus never existed” but was merely a “tool created by smart people to control dumb people.”During a backstage tirade at the Smoothie King Center in New Orleans on Friday, Jay Z pointed around the room saying, “Ya’ll are being played.”"
    print("Running")
    test = second_layer(input_text)
    print(vars(test))

test()
