import itertools
import os
import nltk
import math
import glob
import re

nltk.download('punkt')

def getdoc(path):
    text = []
    filenames = []
    for filename in glob.glob(os.path.join(path, '*.txt')):
        filenames.append(filename)
        files = open(filename, 'r')
        text.append(files.read())
    count = len(text)
    return text, count, filenames

def stopword(path):
    stop_words = []
    with open(path) as f:
        content = f.readlines()
    stop_words = [x.strip() for x in content]

    return stop_words

def tfidf(query, data, stopWords, N):
    words_list = []
    for doc in data:
        doc = re.sub('[^A-Za-z0-9]+',doc)
        words_list.append([word.lower() for word in nltk.word_tokenize(doc) if word not in stopWords])

    all_words = list(itertools.chain(*words_list))
    word_set = list(set(all_words))

    # membuat vector tf
    tf_vecs = [0 for i in range(N)]
    for i in range(N):
        tf_vecs[i] = [words_list[i].count(w) for w in word_set]

    # membuat vector idf
    idf_all_words = list(itertools.chain(*[set(doc_words) for doc_words in words_list]))
    idfs = [math.log(float(N) / idf_all_words.count(w), N) for w in word_set]

    # membuat tf idf
    tfidf = [0 for i in range(N)]
    nomDC = [];
    for i in range(N):
        tfidf[i] = [tf * idf for tf, idf in zip(tf_vecs[i], idfs)]
        nomD = math.sqrt(sum(x**2 for x in tfidf[i]))
        tfidf[i] = [x / nomD for x in tfidf[i]]
        nomDC.append(tfidf[i])

    # mencari nilai query
    query = re.sub('[^A-Za-z0-9]+', ' ', query)
    qwords = [word.lower() for word in query.split() if word not in stopWords]

    # tf vector
    qvec = [qwords.count(w) for w in word_set]

    # tf idf
    qvec = [tf * idf for tf, idf in zip(qvec, idfs)]

    nomQ = math.sqrt(sum(x**2 for x in qvec))

    if nomQ != 0.0:
        qvec = [x / nomQ for x in qvec]
    else:
        qvec = [0 for x in qvec]

    return qvec, nomDC

def cosinsimiliarity(nDoc, nQue):
    result = []
    for i in range(len(nDoc)):
        cosin = []
        for y in range(len(nDoc[0])):
            cosin.append(nDoc[i][y] * nQue[y])
        count = sum(cosin)
        result.append(count)

    return result

def answer(cosin, data, filenames):
    docK = []
    stop = open('univpahlawan/lainnya.txt').read()
    sort = sorted(cosin, reverse=True)

    if sort[0] < 0.1:
        return stop
    
    for x in sort[:1]:
        index = cosin.index(x)
        docK.append(data[index])
        splitname = filenames[index].split('/')
        filejawaban = 'jawaban/'+splitname[-1]
        jawab = open(filejawaban, 'r')

    dec_ans = " ".join(jawab)

    return doc_ans

def main(question):
    initial_query = question.lower()
    stpWrd = stopword('univpahlawan/stopword.txt')
    datas, count_all, filenames = getdoc('univpahlawan')
    qvec_ans, nomD_ans = tfidf(initial_query, datas, stpWrd, count_all)
    cosin_ans = cosinsimiliarity(nomD_ans, qvec_ans)

    doc_rel = answer(cosin_ans, datas, filenames)

    return doc_rel
