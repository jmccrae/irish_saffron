import fileinput
import sys

for line in fileinput.input():
    in_term = False
    for word in line.strip().split(" "):
        w = word[:-2]
        t = word[-1]
        if t == "N":
            if in_term:
                sys.stdout.write("%s_I " % w)
            if not in_term:
                sys.stdout.write("%s_B " % w)
                in_term = True
        elif (t == "A" or t == "D") and in_term:
            sys.stdout.write("%s_I " % w)
        else:
            sys.stdout.write("%s_O " % w)
            in_term = False
    sys.stdout.write("\n")


