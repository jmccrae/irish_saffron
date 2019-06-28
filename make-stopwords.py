import fileinput
from collections import Counter

c = Counter()

for line in fileinput.input():
    for word in line.split(" "):
        c[word] += 1

for word, _ in c.most_common(300):
    print(word)
