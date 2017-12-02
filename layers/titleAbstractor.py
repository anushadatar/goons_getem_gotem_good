#from __future__ import absolute_import
#from __future__ import division, print_function, unicode_literals

from sumy.parsers.html import HtmlParser
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer as Summarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words

import os
from google import google




def crossCheck(self, string)
url = "https://www.cbsnews.com/news/walmart-pulls-rope-tree-journalist-t-shirt-from-site/"
# or for plain text files
# parser = PlaintextParser.from_file("document.txt", Tokenizer(LANGUAGE))
stemmer = Stemmer("english")

summarizer = Summarizer(stemmer)
summarizer.stop_words = get_stop_words("english")


parser = PlaintextParser.from_file(file, Tokenizer("english"))

for sentence in summarizer(parser.document, 1):
    print(sentence)
    sentence = str(sentence)

num_page = 1

search_results = google.search(sentence, num_page)
