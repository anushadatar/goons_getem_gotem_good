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
from bs4 import BeautifulSoup
import requests




url = "https://www.cbsnews.com/news/walmart-pulls-rope-tree-journalist-t-shirt-from-site/"
parser = HtmlParser.from_url(url, Tokenizer("english"))
# or for plain text files
# parser = PlaintextParser.from_file("document.txt", Tokenizer(LANGUAGE))
stemmer = Stemmer("english")

summarizer = Summarizer(stemmer)
summarizer.stop_words = get_stop_words("english")

search = ""

for sentence in summarizer("RTDNA noted in its emailed complaint that nearly three dozen journalists have been assaulted in the U.S. this year “merely for performing their Constitutionally-guaranteed duty to seek and report the truth.” Such messages “inflame the passions” of those who don’t like the media and, at worst, “openly encourage violence targeting journalists,” added the email, written by RTDNA’s executive director, Dan Shelley.", 1):
    print(sentence)
    sentence = str(sentence)

num_page = 1

search_results = google.search(sentence, num_page)
