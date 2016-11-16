class File:

    def __init__(self):
        self.rows = []

    def __init__(self, string_list):
        self.rows = []
        for elem in string_list:
            self.rows.append(elem)

    def change(self, i, j, char):
        last_column = len(self.rows) - 1
        if char == "bs":
            if len(self.rows[i]):
                self.rows[i] = self.rows[i][:j-1] + self.rows[i][j:]
            else:
                self.rows.pop(i)
        elif char == "ent":
            self.rows.insert(i+1,"")
            if self.rows[i][:j]:
                self.rows[i+1] = self.rows[i][j:]
                self.rows[i] = self.rows[i][:j]
        else:
            self.rows[i] = self.rows[i][:j] + char + self.rows[i][j:]





if __name__ == "__main__":
    s1 = "a" * 3
    s2 = "qwqwqwqwqw"
    s3 = ""
    s4 = "asdf"
    l = []
    l.append(s1)
    l.append(s2)
    l.append(s3)
    l.append(s4)
    f = File(l)
    f.change(1,3,"ent")
    for elem in f.rows:
        print elem


