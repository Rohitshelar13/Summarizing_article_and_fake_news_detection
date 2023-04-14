from __future__ import unicode_literals
from flask import Flask,escape,request,render_template
import pickle
from flask import Flask,render_template,url_for,request
from newsapi import NewsApiClient
from spacy_summarization import text_summarizer
# from gensim.summarization import summarize
from genism_summarization import summarize_text
from nltk_summarization import generate_summary_nltk
from sumy_summarization import generate_summary
import time
import spacy
nlp = spacy.load("en_core_web_sm")
app = Flask(__name__)

# Web Scraping Pkg
from bs4 import BeautifulSoup
# from urllib.request import urlopen
from urllib.request import urlopen

# Sumy Pkg
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer

vector = pickle.load(open("vectorizer.pkl",'rb'))
model = pickle.load(open("finalized_model.pkl",'rb'))
@app.route('/')
def home():
    newsapi = NewsApiClient(api_key="dbe14d4568674251a5ad3050d50e0ad0")
    topheadlines = newsapi.get_everything(sources="the-times-of-india",page_size=50,language="en")
 
 
    articles = topheadlines['articles']
 
    desc = []
    news = []
    img = []
    url =[]
 
    for i in range(len(articles)):
        myarticles = articles[i]
        news.append(myarticles['title'])
        desc.append(myarticles['description'])
        img.append(myarticles['urlToImage'])
        url.append(myarticles['url'])
    mylist = zip(news, desc, img,url)
    return render_template('landing.html', context = mylist)

@app.route('/fake_news')
def fake_news():
	return render_template('index_fake.html')

@app.route('/prediction',methods=['GET','POST'])
def prediction():
    if request.method=="POST":
        news = request.form['news']
        predict = model.predict(vector.transform([news]))[0]
        print(predict)
        return render_template("prediction.html",prediction_text="News headline is-> {}".format(predict))
    else:
        return render_template("prediction.html")
    
def sumy_summary(docx):
	parser = PlaintextParser.from_string(docx,Tokenizer("english"))
	lex_summarizer = LexRankSummarizer()
	summary = lex_summarizer(parser.document,3)
	summary_list = [str(sentence) for sentence in summary]
	result = ' '.join(summary_list)
	return result


# Reading Time
def readingTime(mytext):
	total_words = len([ token.text for token in nlp(mytext)])
	estimatedTime = total_words/200.0
	return estimatedTime

# Fetch Text From Url
def get_text(url):
	page = urlopen(url)
	soup = BeautifulSoup(page)
	fetched_text = ' '.join(map(lambda p:p.text,soup.find_all('p')))
	return fetched_text

@app.route('/summary')
def summary():
	return render_template('index.html')


@app.route('/analyze',methods=['GET','POST'])
def analyze():
	start = time.time()
	if request.method == 'POST':
		rawtext = request.form['rawtext']
		final_reading_time = readingTime(rawtext)
		final_summary = text_summarizer(rawtext)
		summary_reading_time = readingTime(final_summary)
		end = time.time()
		final_time = end-start
	return render_template('index.html',ctext=rawtext,final_summary=final_summary,final_time=final_time,final_reading_time=final_reading_time,summary_reading_time=summary_reading_time)

@app.route('/analyze_url',methods=['GET','POST'])
def analyze_url():
	start = time.time()
	if request.method == 'POST':
		raw_url = request.form['raw_url']
		rawtext = get_text(raw_url)
		final_reading_time = readingTime(rawtext)
		final_summary = text_summarizer(rawtext)
		summary_reading_time = readingTime(final_summary)
		end = time.time()
		final_time = end-start
	return render_template('index.html',ctext=rawtext,final_summary=final_summary,final_time=final_time,final_reading_time=final_reading_time,summary_reading_time=summary_reading_time)



@app.route('/compare_summary')
def compare_summary():
	return render_template('compare_summary.html')

@app.route('/comparer',methods=['GET','POST'])
def comparer():
	start = time.time()
	if request.method == 'POST':
		rawtext=""
		rawtext = request.form['rawtext']
		print(rawtext)
		final_reading_time = readingTime(rawtext)
		final_summary_spacy = text_summarizer(rawtext)
		summary_reading_time = readingTime(final_summary_spacy)
		# Gensim Summarizer
		final_summary_gensim = summarize_text(rawtext)
		summary_reading_time_gensim = readingTime(final_summary_gensim)
		# NLTK
		final_summary_nltk = generate_summary_nltk(rawtext)
		summary_reading_time_nltk = readingTime(final_summary_nltk)
		# Sumy
		final_summary_sumy=""
		final_summary_sumy = generate_summary(rawtext)
		# print(listToString(final_summary_sumy))
		summary_reading_time_sumy = readingTime(final_summary_sumy) 

		end = time.time()
		final_time = end-start
	return render_template('compare_summary.html',ctext=rawtext,final_summary_spacy=final_summary_spacy,final_summary_gensim=final_summary_gensim,final_summary_nltk=final_summary_nltk,final_time=final_time,final_reading_time=final_reading_time,summary_reading_time=summary_reading_time,summary_reading_time_gensim=summary_reading_time_gensim,final_summary_sumy=final_summary_sumy,summary_reading_time_sumy=summary_reading_time_sumy,summary_reading_time_nltk=summary_reading_time_nltk)




if __name__ == '__main__':
    app.run()