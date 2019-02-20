def process(filename):
    with open(filename, mode="r") as r:
        content = r.readlines()
    content = sorted(set(content))
    with open(filename, mode="w", newline="\n") as w:
        w.writelines(content)


process("data/free.txt")
process("data/occu.txt")
