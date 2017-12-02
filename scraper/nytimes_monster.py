from newspaper import Article
import newspaper
import requests
import dateutil
from bs4 import BeautifulSoup
import requests
import csv
import numpy
import urllib

site_url = "https://www.nytimes.com/interactive/2017/magazine/past-issues-sunday-mag.html"
site = requests.get(site_url)
soup = BeautifulSoup(site.content, "lxml")

article_title = []
article_text = []
article_label = []
url_array = []
unique = True;
counter = 0
year = "2012"


def find_links(soup, position, key1, key2):
    url_array = []
    unique = True
    for link in soup.find_all('a'):
        url = link.get('href')
        if len(str(url)) > 10:
            url_split = url.split("/")

            if (len(url_split) > position)and((url_split[position] == key1)or(url_split[position] == key2)):
                article_url = url

                for i in range(len(url_array)):
                    if url_array[i] == article_url:
                        unique = False
                if unique:
                    #print(article_url)
                    url_array.append(article_url)
        unique = True
    return url_array

def csv_writer(url):
    a = Article(url)
    a.download()
    if a.html != None:
        a.parse()
        if len(a.text) > 500:
            article_title.append(a.title)
            article_text.append(a.text)
            article_label.append("REAL")

            with open('nytimes_2012.csv', 'a', newline='\n') as csvfile:
                writer = csv.writer(csvfile, delimiter=',')
                writer.writerow([a.title, a.text, "REAL"])

magazines = find_links(soup, 4, year, "lol")
magazines = magazines[1:]


for i in range(len(magazines)):
    magazines_split = magazines[i].split("/")
    magazine_link= requests.get(magazines[i])
    new_soup = BeautifulSoup(magazine_link.content, "lxml")

    print(magazines[i] + '\033[92m')
    print(str(magazines_split[4]))
    articles = find_links(new_soup, 3, year, "lol")
    for j in range(len(articles)):
        print(articles[j] + '\033[94m')
        csv_writer(url = articles[j])
        counter += 1
print(counter)




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
