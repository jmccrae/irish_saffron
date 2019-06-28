import gzip
import xml.etree.ElementTree as ET
import json
from nltk import word_tokenize
from collections import Counter

def read_morphology():
    tree = ET.parse("morphology.xml")
    morph = {}
    for subentry in tree.getroot().iter():
        if subentry.tag == "subentries":
            variants = []
            for entry in subentry.findall("entry"):
                variants.append(entry.findall("src")[0].findall("scope")[0].findall("ortho")[0].findall("token")[0].text.lower())
            for v1 in variants:
                if v1 not in morph:
                    morph[v1] = set([])
                for v2 in variants:
                    morph[v1].add(v2)

    return morph

morph = read_morphology()

terms = [l.strip().split("\t") for l in open("19.03.01-tearma.ie-concepts.txt").readlines()]
terms = set(t[1] for t in terms if len(t) >= 2)


def build_trie(words):
    if len(words) == 0:
        return {"":""}
    else:
        return {words[0]: build_trie(words[1:])}

def trie_merge(trie1, trie2):
    if trie1 == "":
        return trie2
    if trie2 == "":
        return trie1
    m = trie1
    for k in trie2.keys():
        if k in trie1:
            m[k] = trie_merge(trie1[k], trie2[k])
        else:
            m[k] = trie2[k]
    return m
            

def term_trie():
    trie = {}
    for term in terms:
        words = term.lower().split(" ")
        trie = trie_merge(trie, build_trie(words))
    return trie


trie = term_trie()

termfreqs = Counter()

def count(tokens):
    part_matches = []
    for i, token in enumerate(tokens):
        pm_new = []
        for pm in part_matches:
            t = trie
            for x in pm:
                t = t[x]
            z = [t2 for t2 in morph.get(token.lower(), [token.lower()]) if t2 in t]
            if z:
                pm_new.append(pm + z[0:1])

        z = [t2 for t2 in morph.get(token.lower(), [token.lower()]) if t2 in trie]
        if z:
            pm_new.append(z[0:1])

        part_matches = pm_new
        for pm in part_matches:
            t = trie
            for x in pm:
                t = t[x]
            if "" in t:
                termfreqs[" ".join(pm)] += 1

with gzip.open("/home/jmccrae/data/wiki/gawiki-filt.gz", "rt") as input:
    line = input.readline()
    while line:
        doc = line.strip().split(":")
        title = doc[0]
        contents = ":".join(doc[1:])
        tokens = word_tokenize(contents)
        count(tokens)
        line = input.readline()

for term, freq in termfreqs.items():
    print(freq, "\t", term)
