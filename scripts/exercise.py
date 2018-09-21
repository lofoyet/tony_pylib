#!/usr/bin/env python
# coding: utf-8

# In[2]:


import sys
import os


# In[3]:


import pandas as pd
import numpy as np


# In[4]:


sys.path.append("/Users/tonyliu/coop/Bomoda_for_all/bomoda2/fireworks/lib/")


# In[100]:


df = pd.read_csv("data.csv", encoding="utf-8").sort_values("sentiment",
                                                           ascending=False).reset_index(drop=True)

print "finish reading data"
# In[101]:


df.head()


# In[103]:


df.tail()


# In[102]:


df.groupby("sentiment").size()


# In[104]:


# cleaning


# In[105]:


from text_processing import clean_social_text_no_tag


# In[106]:


def clean_data(text):
    return clean_social_text_no_tag(text)


# In[107]:


df["content"] = df["content"].apply(clean_data)


# In[108]:


from tokenize_en import EnglishTokenizer
tokenizer = EnglishTokenizer()


# In[109]:


df["tokens"] = df["content"].apply(tokenizer.tokenize)

print "finish tokenization"

# In[110]:


# remove stop words


# In[111]:


import nltk
from nltk.corpus import stopwords
stopwords = set(stopwords.words('english'))


# In[112]:


def rm_stopwords(tokens, stopwords):
    cleaned = []
    for token in tokens:
        if token not in stopwords:
            cleaned.append(token)
    return cleaned


# In[113]:


df["tokens"] = df["tokens"].apply(
    lambda tokens: rm_stopwords(tokens, stopwords))
print "finish stopwords"


# In[114]:


# bag of words


# In[115]:


bags = {}
for index, tokens in df["tokens"].iteritems():
    for token in tokens:
        if token not in bags:
            bags[token] = len(bags) + 1  # 0 should be padding


# In[116]:


def word_to_index(tokens, bags):
    indices = [0] * (len(bags) + 1)
    for token in tokens:
        indices[bags[token]] = 1
    return indices


# In[117]:


df["index"] = df["tokens"].apply(lambda tokens: word_to_index(tokens, bags))
print "finish index"


# In[118]:


# padding


# In[119]:


longest_len = max(map(len, df["index"]))


# In[120]:


def pad_seq(seq, longest_len):
    if len(seq) < longest_len:
        return np.array(seq + (longest_len - len(seq)) * [0])
    else:
        return np.array(seq[:longest_len])


# In[121]:


df["padded"] = df["index"].apply(lambda seq: pad_seq(seq, longest_len=120))
print "finish padding"


# In[122]:


X, Y = np.stack(df["padded"]), np.asarray(df["sentiment"])


# In[123]:


# split data


# In[124]:


index = df.index.copy().tolist()


# In[94]:


train_num = (df.shape[0] // 10 * 7)
test_num = (df.shape[0] // 10 * 2)
dev_num = (df.shape[0] // 10 * 1)


# In[95]:


np.random.shuffle(index)
train, test, dev = index[:train_num], index[train_num:train_num +
                                            test_num], index[train_num + test_num:train_num + test_num + dev_num]


# In[96]:


# over sampling and under


# In[130]:


train_0 = [t for t in train if t >= 3000]
train_1 = [t for t in train if t < 3000]


# In[137]:


train_0 = np.random.choice(train_0, size=5000, replace=False)
train_1 = np.random.choice(train_1, size=5000, replace=True)


# In[138]:


train = np.concatenate([train_0, train_1])
train.shape


# In[139]:


train_X = X[train]
train_Y = Y[train]
test_X = X[test]
test_Y = Y[test]
dev_X = X[dev]
dev_Y = Y[dev]

print "finish splitting"

# In[140]:


# logistic regression


# In[141]:


from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score, classification_report, precision_score, recall_score,precision_recall_curve,roc_curve


# In[149]:

def lr_train():
    print "start training"
    model = LogisticRegression()
    model.fit(train_X, train_Y)
    print "finish training"
    train_cf = confusion_matrix(train_Y, model.predict(train_X))
    print train_cf
    tn, fp, fn, tp = train_cf.ravel()
    predict_y_test = model.predict(test_X)
    print confusion_matrix(test_Y, predict_y_test)
    print "Logistic Accuracy is %2.2f" % accuracy_score(test_Y, predict_y_test)

# lr_train()

from sklearn.ensemble import RandomForestClassifier

def rf_train():
    print "start training"
    model = RandomForestClassifier(n_estimators=1000, max_depth=None, min_samples_split=10,class_weight="balanced")
    model.fit(train_X, train_Y)
    print "finish training"
    train_cf = confusion_matrix(train_Y, model.predict(train_X))
    print train_cf
    tn, fp, fn, tp = train_cf.ravel()
    predict_y_test = model.predict(test_X)
    print confusion_matrix(test_Y, predict_y_test)
    print "RandomForest Accuracy is %2.2f" % accuracy_score(test_Y, predict_y_test)

# rf_train()

from sklearn.naive_bayes import MultinomialNB

def nb_train():
    print "start training"
    model = MultinomialNB()
    model.fit(train_X, train_Y)
    print "finish training"
    train_cf = confusion_matrix(train_Y, model.predict(train_X))
    print train_cf
    tn, fp, fn, tp = train_cf.ravel()
    predict_y_test = model.predict(test_X)
    print confusion_matrix(test_Y, predict_y_test)
    print "MultinomialNB Accuracy is %2.2f" % accuracy_score(test_Y, predict_y_test)

# nb_train()

from sklearn.svm import SVC

def svm_train():
    print "start training"
    model = SVC()
    model.fit(train_X, train_Y)
    print "finish training"
    train_cf = confusion_matrix(train_Y, model.predict(train_X))
    print train_cf
    tn, fp, fn, tp = train_cf.ravel()
    predict_y_test = model.predict(test_X)
    print confusion_matrix(test_Y, predict_y_test)
    print "SVC Accuracy is %2.2f" % accuracy_score(test_Y, predict_y_test)

# svm_train()

from sklearn.ensemble import AdaBoostClassifier

def boost_train():
    print "start training"
    model = AdaBoostClassifier()
    model.fit(train_X, train_Y)
    print "finish training"
    train_cf = confusion_matrix(train_Y, model.predict(train_X))
    print train_cf
    tn, fp, fn, tp = train_cf.ravel()
    predict_y_test = model.predict(test_X)
    print confusion_matrix(test_Y, predict_y_test)
    print "AdaBoostClassifier Accuracy is %2.2f" % accuracy_score(test_Y, predict_y_test)

# boost_train()

from sklearn.ensemble import BaggingClassifier
def bagging_train():
    print "start training"
    model = BaggingClassifier()
    model.fit(train_X, train_Y)
    print "finish training"
    train_cf = confusion_matrix(train_Y, model.predict(train_X))
    print train_cf
    tn, fp, fn, tp = train_cf.ravel()
    predict_y_test = model.predict(test_X)
    print confusion_matrix(test_Y, predict_y_test)
    print "BaggingClassifier Accuracy is %2.2f" % accuracy_score(test_Y, predict_y_test)

# bagging_train()

from sklearn.neural_network import MLPClassifier

def ann_train():
    print "start training"
    model = MLPClassifier(learning_rate="invscaling")
    model.fit(train_X, train_Y)
    print "finish training"
    train_cf = confusion_matrix(train_Y, model.predict(train_X))
    print train_cf
    tn, fp, fn, tp = train_cf.ravel()
    predict_y_test = model.predict(test_X)
    print confusion_matrix(test_Y, predict_y_test)
    print "MLPClassifier Accuracy is %2.2f" % accuracy_score(test_Y, predict_y_test)

# ann_train()

from sklearn.tree import DecisionTreeClassifier

def tree_train():
    print "start training"
    model = DecisionTreeClassifier()
    model.fit(train_X, train_Y)
    print "finish training"
    train_cf = confusion_matrix(train_Y, model.predict(train_X))
    print train_cf
    tn, fp, fn, tp = train_cf.ravel()
    predict_y_test = model.predict(test_X)
    print confusion_matrix(test_Y, predict_y_test)
    print "tree Accuracy is %2.2f" % accuracy_score(test_Y, predict_y_test)

tree_train()
