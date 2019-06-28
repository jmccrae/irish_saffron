import fileinput
import sys

emap = {
        "N": "N",
        "V": "V",
        "A": "A",
        "R": "R",
        "S": "S",
        "C": "C",
        "P": "P",
        "U": "T",
        "Q": "T",
        "T": "D",
        "D": "D",
        "W": "T",
        "M": "M",
        "Y": "O",
        "X": "O",
        "I": "O",
        "F": "O"
        }

tmap = {
        "N": "N",
        "^": "N",
        "V": "V",
        "A": "A",
        "R": "R",
        "P": "S",
        "O": "P",
        "&": "C",
        "T": "T",
        "D": "D",
        "$": "M",
        "G": "O",
        "@": "O",
        "#": "O",
        ",": "O",
        "E": "O",
        "!": "O",
        "~": "O",
        "U": "O",
        "EN": "O",
        "#MWE": "O",
        "VN": "V"
        }
 


def align(file_name, elaine):
    for line in fileinput.input(file_name):
        for word in line.strip().split(" "):
            w = word[:word.rindex("_")]
            t = word[word.rindex("_") +1:]
            if elaine:
                sys.stdout.write("%s_%s " % (w, emap[t]))
            else:
                sys.stdout.write("%s_%s " % (w, tmap[t]))
        sys.stdout.write("\n")

align("elaine_corpus.txt", True)
align("teresa_twitter_corpus.txt", False)

