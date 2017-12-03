# NewsBlind
## Summary
Machine-learning powered fake news detector with a user-oriented web interface that includes both a concrete judgment on the article, detailed and rigorous summary, and a crowdsourced poll for users to vote on whether or not they agree on the application's judgment.

## Our Hack
We created a multi-layered algorithm which uses machine learning, sentiment analysis, and other facets of natural language processing to holistically evaluate news articles for bias and falsehoods. We created a weighted percentage based on the results of:
* Judgement of the intentions the text based on the results of a natural language processing-powered linear support vector machine (a machine learning algorithm) trained on thousands of real and fake articles acquired via a web crawler
* Response of polarity and subjectivity-based sentiment analysis of the article headline and text
* Judgement of a naive Bayesian classifier (a machine learning algorithm) regarding the extent to which the headline aims to sway the reader
* Grammar analysis of article text
* Cross-Referencing an established database of questionable, problematic, and trustworthy top-level domains and secondary domains.

Then, we created an interface using web technologies such as Flask, Ajax, and HTML/CSS/Javascript to create an in-browser experience which, in response to a user's input, runs the algorithm and returns a detailed summary of the article's performance in terms of the metrics. In addition to this more detailed information, we also provide a comprehensive percentage and progress bar to provide a more direct summary. Furthermore, we have also included a poll for users to comment on whether or not they agree with the machine's judgment: doing so allows for more open communication and democracy, as we do not intend on censoring any information. Instead, our goal is to increase the extent to which citizens understand the sources and elements (and any related biases or falsehoods) associated with consuming media.

In the future, we would love host this project on the internet completely such that users can access it online directly. From there, we could explore options such as browser and social media extensions. It would also be an exciting data science project to incorporate the crowdsourced poll results in the algorithm results.

## About Us
We are NewsBlind, a team of engineers from Olin College of Engineering. Our product is a web app that takes URLs inputted by the user and determines whether the article in question contains false, biased, and/or questionable information. 

Our interconnectedness on the web and the lightning speed at which data is shared creates an environment that makes it very easy for falsehoods and misinformation to spread. Easy access to accurate information on the internet is crucial to the continued success of advancing technology and the success of the human race as a whole. While it is of the utmost importance to minimize the pertinence of fake news, we firmly believe that outright censorship of information is wrong. Our product is aimed at informing viewers about the accuracy of the media they consume, but ultimately leaves the decision up to them whether they wish to view and/or share the article or not.</p>


## How to Install
All of the dependencies for this application exist in the requirements.txt file in this particular directory. To install them, you'll first need python 2.7. Then, if you don't have pip, install pip:
```
sudo apt-get install python-pip
```
Then, you can install the requirements with
```
pip install -r requirements.txt
```

## How to Run
To run this program, clone this repository. To interface with the application, you will need to start the Flask server and open up the HTML pages in your favorite 
Then, navigate to the top directory and run
```
cd layers
python detect_prod.py
```
Then, open up the index.html page located in the /web directory. You can do this from the graphic file structure user interface, or you can use terminal. From terminal, navigate again to the top of the project and run
```
cd web
[browser] index.html
```
From there, the application should work like a usual web page. 
