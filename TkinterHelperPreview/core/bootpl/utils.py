def merge_style(t1, t2):
    t = None
    if t1 != "" or t2 != "":
        t = list()
        if t1 != "":
            t.append(t1)
        if t2 != "":
            t.append(t2)

        t = " ".join(t)
    return t


if __name__ == '__main__':
    print(merge_style("1", "4"))
