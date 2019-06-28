import sys

clazz = {
    "B":{"B":0,"I":0,"O":0},
    "I":{"B":0,"I":0,"O":0},
    "O":{"B":0,"I":0,"O":0}
    }

with open(sys.argv[1]) as gold:
    with open(sys.argv[2]) as output:
        line1 = gold.readline()
        line2 = output.readline()
        while line1 and line2:
            l1 = line1.strip().split(" ")
            l2 = line2.strip().split(" ")
            if len(l1) != len(l2):
                print(l1)
                print(l2)
                first_diff = min(i for i in range(min(len(l1),len(l2))) if l1[i][:-1] != l2[i][:-1])
                print(first_diff, l1[first_diff], l2[first_diff])
                print("Lines don't match")
                sys.exit(-1)
            for w1, w2 in zip(l1, l2):
                clazz[w1[-1:]][w2[-1:]] += 1
            line1 = gold.readline()
            line2 = output.readline()

def clazz_score(c):
    tp = clazz[c][c]
    fp = sum(clazz[c].values()) - tp
    fn = sum(z[c] for z in clazz.values()) - tp
    if tp == 0:
        return 1.0, 0.0, 0.0
    return tp / (tp + fp), tp / (tp + fn), 2.0 * tp / (2.0*tp + fn + fp)

print("|   |    B   |   I    |    O   | Prec  | Recl  |  F-M  |")
p,r,f = clazz_score("B")
print("| B | % 6d | % 6d | % 6d | %.3f | %.3f | %.3f |" % (clazz["B"]["B"], clazz["B"]["I"], clazz["B"]["O"], p, r, f))
p,r,f = clazz_score("I")
print("| I | % 6d | % 6d | % 6d | %.3f | %.3f | %.3f |" % (clazz["I"]["B"], clazz["I"]["I"], clazz["I"]["O"], p, r, f))
p,r,f = clazz_score("O")
print("| O | % 6d | % 6d | % 6d | %.3f | %.3f | %.3f |" % (clazz["O"]["B"], clazz["O"]["I"], clazz["O"]["O"], p, r, f))

