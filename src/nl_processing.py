from collections import Counter
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
import heapq


def find_relevant_terms(text, n = 10):
    """
    Gets the n most frequent words in the text.

    Parameters:
    text (string): The text.
    n (int): The n most frequent words. Defaults to 10.

    Returns:
    collection: The set of the n most frequent words.
    """

    words = word_tokenize(text.lower())
    stop_words = set(stopwords.words('english'))
    filtered_words = [word for word in words if word.isalnum() and word.lower() not in stop_words]
    word_counts = Counter(filtered_words)
    return word_counts.most_common(n)


def generate_summary(text, num_sentences=3):
    """
    Summarizes a text

    Parameters:
    text (string): The text.
    num_sentences (int). The number of sentences produced.
    """
    sentences = sent_tokenize(text)
    clean_sentences = [sentence.lower() for sentence in sentences if sentence.strip() != '']

    stop_words = set(stopwords.words('english'))
    word_freq = {}
    for sentence in clean_sentences:
        words = sentence.split()
        for word in words:
            if word not in stop_words:
                if word not in word_freq.keys():
                    word_freq[word] = 1
                else:
                    word_freq[word] += 1

    max_freq = max(word_freq.values())
    for word in word_freq.keys():
        word_freq[word] = (word_freq[word] / max_freq)

    sent_strength = {}
    for sentence in clean_sentences:
        for word in sentence.split():
            if word in word_freq.keys():
                if len(sentence.split(' ')) < 30:
                    if sentence not in sent_strength.keys():
                        sent_strength[sentence] = word_freq[word]
                    else:
                        sent_strength[sentence] += word_freq[word]

    summary_sentences = heapq.nlargest(num_sentences, sent_strength, key=sent_strength.get)
    summary = ' '.join(summary_sentences)
    
    return summary


