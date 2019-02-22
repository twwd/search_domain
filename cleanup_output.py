def process(filename):
    with open(filename, mode="r") as r:
        content = r.readlines()
    content = sorted(set(content))
    with open(filename, mode="w", newline="\n") as w:
        w.writelines(content)


def merge(in_files, out_file):
    content = set()
    for in_file in in_files:
        with open(in_file, mode="r") as r:
            content.update(r.readlines())
    content = sorted(content)
    with open(out_file, mode="w", newline="\n") as w:
        w.writelines(content)


merge(['data/free.txt', 'data/free_old.txt'], 'data/free.txt')
merge(['data/occu.txt', 'data/occu_old.txt'], 'data/occu.txt')

# process("data/free.txt")
# process("data/occu.txt")
