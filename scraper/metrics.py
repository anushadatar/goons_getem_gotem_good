'''
Step 1: Title/Domain Analysis. If “.wordpress” “.com.co” appear in the title -- or any slight variation on a well known website-- this is usually a sign there is a problem.

Step 2: About Us Analysis. Google every title/domain name/anyone listed in the “About Us” section to see if anyone has previously reported on the website (snopes, hoax-slayer, factcheck.org, etc.) or whether it has a Wikipedia page with citations or something similar detailing its background. This is useful for identifying and correctly categorizing lesser known and/or new websites that may be on the up-and-up, such as satirical sources or websites that are explicit about their political orientation.

Step 3: Source Analysis. Does the website mention/link to a study or source? Look up the source/study. Is it being accurately reflected and reported? Are officials being cited? Can a primary source be located for its quotations? Some media literacy and critical scholars call this triangulation: Verify details, facts, quotes, etc. with multiple sources.

Step 4: Writing Style Analysis. Does the website follow AP Style Guide? Typically, lack of style guide use signifies questionable, more opinion-oriented practices, and may indicate an overall lack of editing or fact-checking process. Does it frequently use ALL CAPS in headlines and/or body text? Does the headline or body of the text use phrases like "WOW!!!!"? This stylistic practice and these types of hyperbolic word choices are often used to create emotional responses with readers that is avoided in more traditional journalism and isn’t something that would be permitted or encouraged by the AP Style Guide

Step 5: Aesthetic Analysis. Like the style-guide, many fake and questionable news sites utilize very bad design. Are screens are cluttered and they use heavy-handed photo-shopping or born digital images?

Step 6: Social Media Analysis. Look up the website on Facebook. Do the headlines and posts rely on sensational or provocative language (aka click-bait) in order to attract attention and encourage likes, click-throughs, and shares? Do the headlines and social media descriptions match or accurately reflect the content of the linked article? (this step isn’t particularly good at helping us find fake news, but it can help us identify other misleading news sources)

By considering all of these areas of information we can determine which category or categories a website may occupy, although all categorizations are by necessity open to discussion and revision. For more information about analyzing the credibility of sources, please see this resource.

Disclaimer The information contained in this site is for informational and educational purposes only. We have made every attempt to ensure that the information contained in this site and in our downloadable data is reliable; however, we are not responsible for any errors, or for the results obtained from the use of this information. All information in this site is provided “as is” and “as available,” with no guarantee of accuracy, reliability, completeness, or of the services or results obtained from the use of this information. By using OpenSources, you expressly agree that the use of OpenSources and its data is at your sole risk.
'''
from newspaper import Article
import newspaper
import requests
import dateutil
from bs4 import BeautifulSoup
import requests
import csv
import numpy
import urllib
import wikipedia
site_url = "http://www.breitbart.com/big-government/2017/12/01/michael-flynn-report-trump-white-house-caught-off-guard-flynn-plea-counsel-didnt-know/"

trusted_domain = 2
about_us = None
source_analysis = True
suspicious_site = 0;
suspicious_TLD = [".country", ".stream", ".gdn", ".mom", ".xin", ".kim",
                    ".men", ".loan", ".download", ".racing", ".online",
                    ".science", ".ren", ".gb", ".win", ".top", ".review",
                    ".vip", ".party", ".tech", ".co.com", ".wordpress"]
safe_TLD = [".com", ".org", ".edu", ".co", ".gov"]
suspicious_websites = []
websites = []
category = []

def find_author(author):
    message = "No substantial information about " + author + " found"
    author_names = author.split(" ")
    if wikipedia.search(author) == None:
        return message
    else:
        if len(wikipedia.search(author)) < 5:
            searches = len(wikipedia.search(author))
        else:
            searches = 5
        for result in wikipedia.search(author):
            content = wikipedia.page(result).content
            if (content.find(author_names[0]) != -1) and (content.find(author_names[-1]) != -1):
                return wikipedia.page(result).summary
            return message




with open('sources.csv', 'r', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
        websites.append(row[0])
        if row[1] == "bias":
            category.append(2)
        elif row[1] == "clickbait":
            category.append(1)
        elif row[1] == "conspiracy":
            category.append(3)
        elif row[1] == "unreliable":
            category.append(4)
        elif row[1] == "fake":
            category.append(7)
        elif row[1] == "political":
            category.append(1)
        elif row[1] == "rumor":
            category.append(3)
        elif row[1] == "junksci":
            category.append(3)
        elif row[1] == "hate":
            category.append(4)
suspicious_websites = [websites, category]

url_split_1 = site_url.split('/')

for i in range(len(suspicious_TLD)):
    if url_split_1[2].find(suspicious_TLD[i]) != -1:
        trusted_domain = 4
        break
if trusted_domain < 1:
    for i in range(len(safe_TLD)):
        if url_split_1[2].find(safe_TLD[i]) != -1:
            trusted_domain = 0;
            break
    """
    url_split_2 = url_split_1[i].split('.')
    for j in range(len(url_split_2)):
        if url_split_2[j] == "com" or "org" or "edu" or "co" or "gov":
            trusted_domain = True
    """
for i in range(len(websites)):
    if (url_split_1[2]).find(websites[i]) != -1:
        suspicious_site = True
        suspicious_site = category[i]
        break

total_score = trusted_domain + suspicious_site
print(total_score)
a = Article(site_url)
a.download()
a.parse()


authors = a.authors
for author in authors:
    print(find_author(author))
