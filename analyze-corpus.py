import fileinput
import collections

stats = {}

for line in fileinput.input():
    for word in line.strip().split(" "):
        w = word[:word.rindex("_")]
        t = word[word.rindex("_") + 1:]
        if t not in stats:
            stats[t] = collections.Counter()
        stats[t][w] += 1

n_words = sum(sum(c.values()) for t, c in stats.items())

for t, c in stats.items():
    print("%s\t%d (%.2f%%)\t%s" % (t, sum(c.values()), sum(c.values())/n_words, ", ".join(x[0] for x in c.most_common(10))))

