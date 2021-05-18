import os
from typing import List

class TableFileLoader:

    def loadFile(self, filename: str) -> object:
        if os.path.isfile(filename) and "chr" in filename:
            file = open(filename, 'r')
            fileContent = []
            temp = {}

            for line in file:
                fileContent.append(line.replace('\n', '').split('\t'))
            for item in fileContent[0]:
                temp[item] = []
            for i, item in enumerate(fileContent[0]):
                temp[item].extend([x[i] if len(x) > i else "" for x in fileContent[1:-1]])

            file.close()
            return temp


class TableFileLoader2:

    def loadFile(self, filename: str) -> List:
        if os.path.isfile(filename) and "chr" in filename:
            file = open(filename, 'r')
            fileContent = []
            header = []

            for line in file:
                fileContent.append(line.replace('\n', '').split('\t'))
            for item in fileContent[0]:
                header.append(item)
            temp = []

            for item in fileContent[1:-1]:
                x = {h: item[i] if len(item) > i else "" for i, h in enumerate(header)}
                temp.append(x)

            file.close()
            return temp

class TestClass (TableFileLoader2):

    def exec(self, filename):
        temp = self.loadFile(filename)
        for item in temp:
            print(item)

if __name__ == "__main__":
    test = TestClass().exec("c:\\temp\\results\\04180001-bs_12_chr.txt")

