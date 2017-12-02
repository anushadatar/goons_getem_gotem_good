#!/usr/bin/env python
# -*- coding: utf-8 -*-
from textblob import TextBlob

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
        self.text = TextBlob(self.raw_text)
        self.polarity = text_blob.sentiment[0]
        self.subjectivity = subtext_blob.sentiment[1]
        self.sentiment_metric = compute_sentiment_metric(self)

    def compute_sentiment_metric(self):
        """
        Turns string of article text body into a sentiment percentage. The higher
        the overall polairty (positive/negative bias) or 
        """
        return ((abs(self.polarity) + self.subjectivity)/2)*100
