from newspaper import Article
import newspaper
import requests
import dateutil
from bs4 import BeautifulSoup
import requests
import csv
import numpy
import urllib


num_articles = 0;
site_url = "https://www.nytimes.com/section/science"
site = requests.get(site_url)
soup = BeautifulSoup(site.content, "lxml")

article_title = []
article_text = []
article_label = []
url_array = []
unique = True;

for link in soup.find_all('a'):
    url = link.get('href')
    if len(url) > 10:
        url_split = url.split("/")
        #print(url)

        if (len(url_split) > 3)and(url_split[3] == "2017"):
            article_url = url

            for i in range(len(url_array)):
                if url_array[i] == article_url:
                    unique = False
            if unique:
                print(article_url)
                url_array.append(article_url)
                a = Article(article_url)
                a.download()
                a.parse()
                if len(a.text) > 500:
                    article_title.append(a.title)
                    article_text.append(a.text)
                    article_label.append("REAL")
                    num_articles += 1

                    csv_array = [article_title, article_text, article_label]
                    with open('nytimes_science.csv', 'a', newline='\n') as csvfile:
                        writer = csv.writer(csvfile, delimiter=',')
                        writer.writerow([a.title, a.text, "REAL"])
    unique = True
