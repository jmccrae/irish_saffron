import fileinput
import sys
import re

word = re.compile("<w.*tag\s*=\s*\"(\w+)\".*std.*=.*\"(\w+)\".*")


def process_file(file_name):
    for line in fileinput.input(file_name):
        m = word.match(line)
        if m:
            tag = m.group(1)
            form = m.group(2)
            if tag == "Nv":
                sys.stdout.write("%s_V " % form)
            else:
                sys.stdout.write("%s_%s " % (form, tag[0]))
        elif line.strip() == "</s>":
            sys.stdout.write("\n")

process_file("POS_DEV.xml")
process_file("POS_TEST.xml")
