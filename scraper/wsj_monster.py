from newspaper import Article
import newspaper
import requests
import dateutil
from bs4 import BeautifulSoup
import requests
import csv
import numpy
import urllib

site_url = "http://www.wsj.com/public/page/archive-2014-1-1.html"
site = requests.get(site_url)
soup = BeautifulSoup(site.content, "lxml")

article_title = []
article_text = []
article_label = []
url_array = []
unique = True;
counter = 0
year = "2014"


def find_links(soup, position, key1, key2):
    url_array = []
    unique = True
    for link in soup.find_all('a'):
        url = link.get('href')
        if len(str(url)) > 10:
            url_split = url.split("/")

            if (len(url_split) > position)and((url_split[position].find(key1) != -1)or(url_split[position].find(key2) != -1)):
                article_url = url

                for i in range(len(url_array)):
                    if url_array[i] == article_url:
                        unique = False
                        break
                if unique:
                    #print(article_url)
                    url_array.append(article_url)
        unique = True
    return url_array

def csv_writer(url):
    print('\033[93m' + url)
    try:
        a = Article(url)
        a.download()
        if a.html != None:
                a.parse()
    except Exception as e:
        return None
    if len(a.text) > 200:
        article_title.append(a.title)
        article_text.append(a.text)
        article_label.append("REAL")
        print('\033[94m' + articles[j])

        with open('../../yhack training data/wsj_2014.csv', 'a', newline='\n') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerow([a.title, a.text, "REAL"])

magazines = find_links(soup, 5, year, "lol")
magazines = magazines[1:]


for i in range(len(magazines)):
    magazines_split = magazines[i].split("/")
    magazine_link= requests.get(magazines[i])
    new_soup = BeautifulSoup(magazine_link.content, "lxml")

    print('\033[92m' + magazines[i])
    articles = find_links(new_soup, 3, "articles", "lol")
    for j in range(len(articles)):
        csv_writer(url = articles[j])
        counter += 1
print(counter)
