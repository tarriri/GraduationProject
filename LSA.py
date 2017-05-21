import sys
import math
from nltk.tokenize import word_tokenize
import snowballstemmer
from nltk.corpus import stopwords
import NewsAnalysisDatabase as db
import numpy

stemmer = snowballstemmer.stemmer("turkish")
stopwords = set(stopwords.words("turkish"))
stopwords.update(['.', ',', '"', "'", "''", '""', '?', '!', ':', ';', '(', ')', '[', ']', '{', '}'])
result_id = db.create_lsa_result()
sample_data, url_list = db.get_sample_document_list()
for i in range(len(url_list)):
    db.create_lsa_data_set(result_id, sample_data[i], url_list[i])


def get_term_array():
    terms = set()
    for i in range(len(sample_data)):
        terms.update(
            [stemmer.stemWord(token) for token in word_tokenize(sample_data[i].lower()) if token not in stopwords])
    return terms


def get_term_document_matrix(tokens):
    term_document = []
    for i in range(len(tokens)):
        term_document.append([])
        term_document[i] = [sample_data[doc_index].count(tokens[i]) for doc_index in range(len(sample_data))]
    return term_document


def get_term_frequency(tokens):
    term_freq = []
    for i in range(len(tokens)):
        term_freq.append([])
        term_freq[i] = [sample_data[doc_index].count(tokens[i]) /
                        len([token for token in word_tokenize(sample_data[doc_index].lower()) if
                             token not in stopwords])
                        for doc_index in range(len(sample_data))]
    return term_freq


def get_inverse_document_frequency(tokens, term_doc):
    inverse_document_freq = [0] * len(tokens)
    for i in range(len(tokens)):
        inverse_document_freq[i] = math.log(len(sample_data) /
                                            (1 + len([doc_index for doc_index in range(len(sample_data)) if
                                                      term_doc[i][doc_index] > 0])))
    return inverse_document_freq


def get_tf_idf(tokens, term_freq, inverse_doc_freq):
    tfidfvector = []
    for i in range(len(tokens)):
        tfidfvector.append([])
        tfidfvector[i] = [term_frequency * inverse_doc_freq[i] for term_frequency in term_freq[i]]
    return tfidfvector


if __name__ == "__main__":
    term_list = list(get_term_array())
    term_list.sort()
    td = get_term_document_matrix(term_list)
    tf = get_term_frequency(term_list)
    idf = get_inverse_document_frequency(term_list, td)
    tfidf = get_tf_idf(term_list, tf, idf)
    U, s, V = numpy.linalg.svd(tfidf, full_matrices=True)

    token_scores = U[:, 0]
    u = numpy.array(token_scores).argsort()[::-1][:20]

    keywords = ""
    for i in range(len(u)):
        keywords += term_list[u[i]]
        if i is not len(u)-1:
            keywords += ", "

    db.update_lsa_result(result_id, keywords)

    exit()



