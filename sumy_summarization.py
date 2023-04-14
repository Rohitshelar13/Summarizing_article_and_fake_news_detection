# from sumy.parsers.plaintext import PlaintextParser
# from sumy.nlp.tokenizers import Tokenizer
# from sumy.summarizers.lsa import LsaSummarizer
# from sumy.nlp.stemmers import Stemmer
# from sumy.utils import get_stop_words
# from nltk.tokenize import sent_tokenize

# def sumy_summarizer(text):
#     # Initialize a parser with the given text
#     text = sent_tokenize(text)
#     parser = PlaintextParser.from_string(text, Tokenizer("english"))
    
#     # Initialize an LSA summarizer with stemmer and stop words
#     summarizer = LsaSummarizer(Stemmer("english"))
#     summarizer.stop_words = get_stop_words("english")
    
#     # Generate the summary
#     summary = summarizer(parser.document, sentences_count=4)
    
#     # Combine the sentences in the summary into a single string and return it
#     summary_text = ""
#     for sentence in summary:
#         summary_text += str(sentence) + " "
#     return summary_text

from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer

from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer

def generate_summary(text):
    # Create a plaintext parser and tokenize the text
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    
    # Create a LexRank summarizer and generate a summary with 3 sentences
    summarizer = LexRankSummarizer()
    summary = summarizer(parser.document, sentences_count=3)
    
    # Combine the sentences into a single string
    summary_text = " ".join(str(sentence) for sentence in summary)
    
    return summary_text