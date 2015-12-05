
def remove_invalid_chars(filename):
    return "".join(i for i in filename if i not in r'\/:*?"<>|')