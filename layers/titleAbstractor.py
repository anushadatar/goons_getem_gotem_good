#from __future__ import absolute_import
#from __future__ import division, print_function, unicode_literals

from sumy.parsers.html import HtmlParser
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer as Summarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words

from google import google




def crossCheck():
    url = "https://www.cbsnews.com/news/walmart-pulls-rope-tree-journalist-t-shirt-from-site/"
    # or for plain text files
    # parser = PlaintextParser.from_file("document.txt", Tokenizer(LANGUAGE))

    fileName = "Article.txt"
    file = open(fileName, "w")


    stemmer = Stemmer("english")

    summarizer = Summarizer(stemmer)
    summarizer.stop_words = get_stop_words("english")


    parser = PlaintextParser.from_file(file, Tokenizer("english"))

    for sentence in summarizer(parser.document, 1):
        print(sentence)
        sentence = str(sentence)

    search_results = google.search(sentence, 1)
    print(search_results)

crossCheck()
