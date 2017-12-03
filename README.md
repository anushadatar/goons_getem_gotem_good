# NewsBlind
YHack 2017 Project. Fake news detector for online websites written in Python 2.7 with Flask server with browser interface in HTML/CSS/Javascript. Motivated by the current political and media situation as well as the challenge issues by the Poynter institute, we aimed to create a hack which 

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
