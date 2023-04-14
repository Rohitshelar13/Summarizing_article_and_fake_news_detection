# import nltk
# from nltk.corpus import stopwords
# from nltk.tokenize import word_tokenize, sent_tokenize
# import heapq  

# def nltk_summarizer(raw_text):
# 	stopWords = set(stopwords.words("english"))
# 	word_frequencies = {}  
# 	for word in nltk.word_tokenize(raw_text):  
# 	    if word not in stopWords:
# 	        if word not in word_frequencies.keys():
# 	            word_frequencies[word] = 1
# 	        else:
# 	            word_frequencies[word] += 1

# 	maximum_frequncy = max(word_frequencies.values())

# 	for word in word_frequencies.keys():  
# 	    word_frequencies[word] = (word_frequencies[word]/maximum_frequncy)

# 	sentence_list = nltk.sent_tokenize(raw_text)
# 	sentence_scores = {}  
# 	for sent in sentence_list:  
# 	    for word in nltk.word_tokenize(sent.lower()):
# 	        if word in word_frequencies.keys():
# 	            if len(sent.split(' ')) < 30:
# 	                if sent not in sentence_scores.keys():
# 	                    sentence_scores[sent] = word_frequencies[word]
# 	                else:
# 	                    sentence_scores[sent] += word_frequencies[word]



# 	summary_sentences = heapq.nlargest(7, sentence_scores, key=sentence_scores.get)

# 	summary = ' '.join(summary_sentences)  
# 	return summary

import nltk
from nltk.tokenize import sent_tokenize
from nltk.probability import FreqDist
from heapq import nlargest

def generate_summary_nltk(text):
    # Tokenize the input text into sentences
    sentences = sent_tokenize(text)
    
    # Create a frequency distribution of the words in the text
    word_frequencies = FreqDist(nltk.word_tokenize(text))
    
    # Get the 10 most frequent words in the text
    most_frequent_words = nlargest(10, word_frequencies, key=word_frequencies.get)
    
    # Create a list to hold the summary sentences
    summary_sentences = []
    
    # Loop through the sentences and score them based on the frequency of the most frequent words they contain
    for sentence in sentences:
        sentence_words = nltk.word_tokenize(sentence.lower())
        score = 0
        for word in most_frequent_words:
            if word in sentence_words:
                score += word_frequencies[word]
        summary_sentences.append((sentence, score))
    
    # Sort the summary sentences in descending order of score
    summary_sentences = sorted(summary_sentences, key=lambda x: x[1], reverse=True)
    
    # Select the top half of the sentences to include in the summary
    num_summary_sentences = len(summary_sentences) // 2
    summary_sentences = summary_sentences[:5]
    
    # Combine the summary sentences into a single string
    summary_text = " ".join(sentence for sentence, score in summary_sentences)
    
    return summary_text