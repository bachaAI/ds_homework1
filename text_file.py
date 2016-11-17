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

    # name in format "name.txt"
    def upload_to_txt(self, name):
        if name.split(".")[-1] != "txt":
            name += ".txt"

        txt_file = open(name, "w")
        for i in self.rows:
            txt_file.write(i + '\n')
        txt_file.close()
        print "File was uploaded to " + name

    # name in format "name.txt"
    def download_from_txt(self, name):
        if name.split(".")[-1] != "txt":
            name += ".txt"
        with open(name) as f:
            for line in f:
                self.rows.append(line[:-1])

if __name__ == "__main__":
    s1 = "a" * 100
    s2 = "q" * 100
    s3 = "w" * 100
    l = []
    l.append(s1)
    l.append(s2)
    l.append(s3)
    f = File(l)
    f.insert(0, 12, "b")
    for elem in f.rows:
        print elem

pass