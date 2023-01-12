import json

import functions_framework
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet

nltk.data.path.append('nltk_data/')


# nltk.download('averaged_perceptron_tagger', download_dir='./nltk_data')
# nltk.download('wordnet', download_dir='./nltk_data')


def lemmatize_words(corpus):
    """
    This function uses the NLTK library to POS tag words and then lemmatize them
    :param corpus: corpus is a set of words devided by "|". i.e The|cats|are|sitting|on|the|couch
    :return:
    """
    # Tokenize the corpus
    tokens = corpus.split("|")

    # POS tag the tokens
    tagged_tokens = nltk.pos_tag(tokens)

    # Initialize the lemmatizer
    lemmatizer = WordNetLemmatizer()

    # Define a function to get the correct POS tag
    def get_wordnet_pos(tag):
        if tag.startswith('J'):
            return wordnet.ADJ
        elif tag.startswith('V'):
            return wordnet.VERB
        elif tag.startswith('N'):
            return wordnet.NOUN
        elif tag.startswith('R'):
            return wordnet.ADV
        else:
            return wordnet.NOUN

    # Iterate through the tagged tokens and lemmatize each word
    lemmas = [lemmatizer.lemmatize(token, get_wordnet_pos(tag)) for token, tag in tagged_tokens]

    return "|".join(lemmas)


@functions_framework.http
def lemmatize(request):
    """
    Defines translate Google Cloud Function
    :param request:
    :return:
    """
    request_json = request.get_json()
    calls = request_json['calls']
    replies = []
    for call in calls:
        text = call[0]
        rs = lemmatize_words(text)
        replies.append(rs)

    return json.dumps({'replies': replies})
