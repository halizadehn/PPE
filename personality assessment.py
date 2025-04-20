import ast
import os
import re
import string
import sys
import pandas as pd
from csv import register_dialect
import numpy as np
from gensim.models import KeyedVectors
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
dataset_dir = "Data/"


def load_predefined_vectors(filepath):
    vectors = {}
    with open(filepath, 'rt') as fp:
        for line in fp:
            key, payload = line.strip().split(':')
            words = payload.split()
            vectors[key] = words
    return vectors


def compute_sim(term, weight, vec, sim_sc_vec, sim_idx_vec, word_embb):
    dim = word_embb.vector_size
    for factor, components in vec.items():
        idx = sim_idx_vec[factor]
        for word in components:
            if (word in word_embb) and (term in word_embb):
                v_a = word_embb[word].reshape(1, dim)
                v_b = word_embb[term].reshape(1, dim)
                sim = weight * cosine_similarity(v_a, v_b)[0][0]
                sim_sc_vec[factor][idx] = sim
                idx += 1
        sim_idx_vec[factor] = idx


def vsm(idx2term, term_doc_mtx, pb5_vec, word_embb):
    x = np.zeros((term_doc_mtx.shape[0], 10), dtype=np.float32)
    for doc_idx, doc in enumerate(term_doc_mtx):
        print('Processing doc_idx {:d}'.format(doc_idx))
        sys.stdout.flush()

        sim_sc_pb5 = {}
        sim_idx_pb5 = {}
        for factor, components in pb5_vec.items():
            sim_sc_pb5[factor] = np.zeros(np.count_nonzero(doc) * len(components), dtype=np.float32)
            sim_idx_pb5[factor] = 0

        for t_i, w in enumerate(doc):
            if w > 0:
                t = idx2term[t_i]
                compute_sim(t, w, pb5_vec, sim_sc_pb5, sim_idx_pb5, word_embb)

        for ft_idx, (factor, sim) in enumerate(sim_sc_pb5.items()):
            idx = sim_idx_pb5[factor]
            x[doc_idx][ft_idx] = sim[:idx].mean()

    return x


def personality_assessment():
    pb5_vec = load_predefined_vectors(dataset_dir+'pb5.txt')
    corpus = []
    users = []
    register_dialect('tab', delimiter='\t')
    df = pd.read_csv(dataset_dir + 'tweets_users.csv', index_col=False, header=None)
    df.columns = ["user_id", "user_text"]
    for i in range(len(df)):
            uid = df.loc[i, "user_id"]
            content = df.loc[i, "user_text"]
            corpus.append(content)
            users.append(uid)
    vectorizer = TfidfVectorizer() # vectorizer = CountVectorizer()
    term_doc_mtx = vectorizer.fit_transform(corpus).toarray()
    idx2term = vectorizer.get_feature_names_out()
    print(' -- Term-Doc Matrix Created --')

    word_embb = KeyedVectors.load_word2vec_format(dataset_dir+"GoogleNews-vectors-negative300.bin.gz", binary=True)
    print(' -- Word Embeddings loaded --')

    x = vsm(idx2term, term_doc_mtx, pb5_vec, word_embb)
    np.nan_to_num(x, copy=False)
    np.save(dataset_dir + "personality_scores", x)
