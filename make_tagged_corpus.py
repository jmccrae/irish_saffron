import gzip
import xml.etree.ElementTree as ET
import json
from nltk import word_tokenize

def init_variations(word):
    if len(word) <= 1:
        return [word]
    elif word[0] == "b":
        return [word, word[0] + "h" + word[1:], "m" + word]
    elif word[0] == "c":
        return [word, word[0] + "h" + word[1:], "g" + word]
    elif word[0] == "d":
        return [word, word[0] + "h" + word[1:], "n" + word]
    elif word[0] == "f":
        return [word, word[0] + "h" + word[1:], "bh" + word]
    elif word[0] == "g":
        return [word, word[0] + "h" + word[1:], "n" + word]
    elif word[0] == "m":
        return [word, word[0] + "h" + word[1:]]
    elif word[0] == "p":
        return [word, word[0] + "h" + word[1:], "b" + word]
    elif word[0] == "s" and word[1] not in ["b","c","d","f","g","l","m","n","p","t"]:
        return [word, word[0] + "h" + word[1:], "t" + word]
    elif word[0] == "t":
        return [word, word[0] + "h" + word[1:], "d" + word]
    elif word[0] in ["a","e","i","o","u"]:
        return [word, "h" + word, "n-" + word]
    else:
        return [word]

def read_morphology():
    tree = ET.parse("morphology.xml")
    morph = {}
    for entry in tree.getroot().findall("entry"):
        lemma = entry.findall("src")[0].findall("scope")[0].findall("ortho")[0].findall("token")[0].text.lower()
        for subentry in entry.findall("subentries"):
            variants = [lemma]
            for entry2 in subentry.findall("entry"):
                variants.append(entry2.findall("src")[0].findall("scope")[0].findall("ortho")[0].findall("token")[0].text.lower())
            for v1 in variants:
                if v1 not in morph:
                    morph[v1] = set([])
                morph[v1].add(lemma)

    return morph

morph = read_morphology()

morph2 = {k2: v for k, v in morph.items() for k2 in init_variations(k) }

morph.update(morph2)

terms = [l.strip().split("\t") for l in open("term_freq-sort.tsv").readlines()]
terms = set(t[1].strip() for t in terms if len(t) >= 2)

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

def get_tags(tokens):
    tags = ["O"] * len(tokens)
    part_matches = []
    for i, token in enumerate(tokens):
        pm_new = []
        for pm in part_matches:
            t = trie
            for x in pm:
                t = t[x]
            z = [t2 for t2 in morph.get(token.lower(), [token.lower()]) if t2 in t]
            for z2 in z:
                if z2 in t:
                    pm_new.append(pm + [z2])

        z = [t2 for t2 in morph.get(token.lower(), [token.lower()]) if t2 in trie]
        for z2 in z:
            if z2 in trie:
                pm_new.append([z2])

        part_matches = pm_new
        for pm in part_matches:
            t = trie
            for x in pm:
                t = t[x]
            if "" in t:
                if tags[i - len(pm) + 1] == "O":
                    tags[i-len(pm)+1] = "B"
                for j in range(i - len(pm)+2, i+1):
                    tags[j] = "I"
                if len(pm) != 1:
                    tags[i] = "I"
                    
    return tags

with gzip.open("gawiki-filt.gz", "rt") as input:
    line = input.readline()
    while line:
        doc = line.strip().split(":")
        title = doc[0]
        contents = ":".join(doc[1:])
        tokens = word_tokenize(contents)
        tags = get_tags(tokens)
        print(" ".join(["%s_%s" % (token, tags[i]) for i, token in enumerate(tokens)]))
        line = input.readline()
