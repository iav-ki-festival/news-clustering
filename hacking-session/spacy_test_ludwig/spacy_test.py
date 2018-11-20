# -*- coding: utf-8 -*-
"""
Created on Sat Nov 10 22:13:26 2018

Test of NLP Library SpaCy

@author: LBartsch
"""

import spacy
from spacy.lang.de import German
import re
from collections import Counter
from websitescraping import simple_get
from bs4 import BeautifulSoup

def cleanup(token, lower = True):
    if lower:
       token = token.lower()
    return token.strip()


def findEntities(document):
    labels = set([w.label_ for w in document.ents]) 
    #print(str(list(labels)))
    ent_dict = {}
    for label in labels: 
        entities = [cleanup(e.string, lower=False) for e in document.ents if label==e.label_] 
        #print(entities)
        entities = list(set(entities)) 
        partial_dict = {label : entities}
        ent_dict.update(partial_dict)
    return ent_dict
        

# return all noun - adjective pairs
def nounAdjectivePairs(doc):
    noun_adj_pairs = []
    for i,token in enumerate(doc):
        if token.pos_ not in ('NOUN','PROPN'):
            continue
        for j in range(i+1,len(doc)):
            if doc[j].pos_ == 'ADJ':
                noun_adj_pairs.append((str(token),str(doc[j])))
                break
    return noun_adj_pairs

# check all adjectives used with a word 
def pos_words (sentence, token, ptag):
    sentences = [sent for sent in sentence.sents if token in sent.string]     
    pwrds = []
    for sent in sentences:
        for word in sent:
            for character in word.string: 
                   pwrds.extend([child.string.strip() for child in word.children
                                                      if child.pos_ == ptag] )
    c = Counter(pwrds).most_common(20)
    return c


url = 'http://iav.de'
raw_html = simple_get(url)

# parsing html
html = BeautifulSoup(raw_html, 'html.parser')

# save text within a paragraph 'p' tag as a list
text_from_html = []
for p in html.select('p'): 
    #replace newline or tab with space
    clean_txt = re.sub("\n|\t", ' ', p.text)
    text_from_html.append(clean_txt)
    print(p.text)


# obsolete - already downloaded manually
#!{sys.executable} -m spacy download de # only for jpython notebook
nlp = spacy.load('de_core_news_sm')
doc = nlp(str(text_from_html))

# number of sentences
count_sents = len(list(doc.sents))

# what entities are in the text? 
entities = findEntities(doc)

# what adjectives are related to what nouns
noun_adjective_pairs = nounAdjectivePairs(doc)

# what adjectives are related to certain nouns
IAV_adjectives = pos_words(doc, 'IAV', 'ADJ')
Fahrzeuge_adjectives = pos_words(doc, 'Fahrzeuge', 'ADJ')