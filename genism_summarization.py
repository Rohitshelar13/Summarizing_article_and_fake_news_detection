import nltk
from nltk.tokenize import sent_tokenize
from gensim.summarization import summarize

def summarize_text(text):
    sentences = sent_tokenize(text)
    if len(sentences) < 2:
        return "Input text is too short for summarization"
    else:
        preprocessed_text = ' '.join(sentences)
        summary = summarize(preprocessed_text, ratio=0.2, split=True)
        summary = ' '.join(summary)
        return summary