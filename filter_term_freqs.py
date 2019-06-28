import xml.etree.ElementTree as ET


def read_pos():
    tree = ET.parse("morphology.xml")
    morph = {}
    for subentry in tree.getroot().findall("entry"):
        for src in subentry.findall("src"):
            if src.findall("scope")[0].findall("tag"):
                pos = src.findall("scope")[0].findall("tag")[0].attrib["tag"]
                word = src.findall("scope")[0].findall("ortho")[0].findall("token")[0].text.lower()
                if word not in morph:
                    morph[word] = [pos]
                else:
                    morph[word].append(pos)
    return morph

pos = read_pos()

with open("term_freqs.tsv") as input:
    line = input.readline()
    while line:
        freq = int(line.split("\t")[0])
        term = line.split("\t")[1].strip().split(" ")

        if term[0] in pos and ("nm" in pos[term[0]] or "nf" in pos[term[0]]) and freq < 3000:
            print(line.strip())
        elif term[0] not in pos and freq < 100:
            print(line.strip())

        line = input.readline()
