#from __future__ import absolute_import
#from __future__ import division, print_function, unicode_literals

from sumy.parsers.html import HtmlParser
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer as Summarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words

import nltk
import grammar_check



url = "https://www.wired.com/story/uber-waymo-gm-infiniti-lucid/"
parser = HtmlParser.from_url(url, Tokenizer("english"))
# or for plain text files
# parser = PlaintextParser.from_file("document.txt", Tokenizer(LANGUAGE))
stemmer = Stemmer("english")

summarizer = Summarizer(stemmer)
summarizer.stop_words = get_stop_words("english")

search = ""

for sentence in summarizer(parser.document, 1):
    sentence = str(sentence)
    tokens = nltk.word_tokenize(sentence)
    tagged = nltk.pos_tag(tokens)

    for element in tagged:
        if element[1] == 'NNP' or element[1] == 'NNPS' or element[1] == 'NN' or element[1] == 'VB' or element[1] == 'VBD' or element[1] == 'VBG' or element[1] == 'VBN' or element[1] == 'VBP' or element[1] == 'VBZ':
            search += element[0] + " "

search = str(search)

tool = grammar_check.LanguageTool('en-GB')
matches = tool.check(search)
new = grammar_check.correct(search, matches)
print(search)
