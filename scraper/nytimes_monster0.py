from newspaper import Article
import newspaper
import requests
import dateutil
from bs4 import BeautifulSoup
import requests
import csv
import numpy
import urllib

site_url = "https://www.nytimes.com/2016/12/16/magazine/the-12-416-issue.html?ref=magazine"
site = requests.get(site_url)
soup = BeautifulSoup(site.content, "lxml")

article_title = []
article_text = []
article_label = []
url_array = []
unique = True;

def find_links(soup, position, key1, key2, color):
    url_array = []
    unique = True
    for link in soup.find_all('a'):
        url = link.get('href')
        if len(url) > 10:
            url_split = url.split("/")

            if (len(url_split) > position)and((url_split[position] == key1)or(url_split[position] == key2)):
                article_url = url

                for i in range(len(url_array)):
                    if url_array[i] == article_url:
                        unique = False
                if unique:
                    print(article_url + color)
                    url_array.append(article_url)
        unique = True
    return url_array

def csv_writer(url, nytimes_monster):
    a = Article(url)
    a.download()
    a.parse()
    if len(a.text) > 500:
        article_title.append(a.title)
        article_text.append(a.text)
        article_label.append("REAL")

        with open(nytimes_monster, 'a', newline='\n') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerow([a.title, a.text, "REAL"])

magazines = find_links(soup, 3, "2016", "indexes", '\033[94m')
print(magazines)



"""
for link in soup.find_all('a'):
    url = link.get('href')
    if len(url) > 10:
        url_split = url.split("/")
        print(url)

        if (len(url_split) > 3)and((url_split[3] == "issue")or(url_split[3] == "indexes")):
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

                    csv_array = [article_title, article_text, article_label]
                    with open('nytimes_science.csv', 'a', newline='\n') as csvfile:
                        writer = csv.writer(csvfile, delimiter=',')
                        writer.writerow([a.title, a.text, "REAL"])
    unique = True
"""
