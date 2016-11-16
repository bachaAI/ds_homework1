class File:

    def __init__(self):
        self.rows = [""]

    def __init__(self, string_list):
        self.rows = []
        for elem in string_list:
            self.rows.append(elem)

    def insert(self, i, j, char):
        if len(self.rows[i]) < 100:
            self.rows[i] = self.rows[i][:j] + char + self.rows[i][j:]
        else:
            self.rows[i] = self.rows[i][:j] + char + self.rows[i][j:]
            tail = self.rows[i][100]
            for k in range(i+1,len(self.rows)):
                self.rows[k] = tail + self.rows[k]
                if len(self.rows[k]) == 101:
                    tail = self.rows[k][100]
                    if k == len(self.rows) - 1:
                        self.rows.append("")
                        self.rows[-1] = tail + self.rows[-1]
                else:
                    break




if __name__ == "__main__":
    s1 = "a" * 100
    s2 = "q" * 100
    s3 = "w" * 100
    l = []
    l.append(s1)
    l.append(s2)
    l.append(s3)
    f = File(l)
    f.insert(0,12,"b")
    for elem in f.rows:
        print elem


