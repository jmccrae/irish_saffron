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
        return [word, "h" + word, "n-" + word, "t-" + word]
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

for k, vs in morph.items():
    print("%s\tB\t%s" % (k, list(vs)[0]))
    print("%s\tI\t%s" % (k, list(vs)[0]))
    print("%s\tO\t%s" % (k, list(vs)[0]))
    print("%s\tN\t%s" % (k, list(vs)[0]))
    print("%s\tV\t%s" % (k, list(vs)[0]))
    print("%s\tA\t%s" % (k, list(vs)[0]))
    print("%s\tR\t%s" % (k, list(vs)[0]))
