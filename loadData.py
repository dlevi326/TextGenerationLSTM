
import json
import os
import string

def loadData(pathname, numLimit = -1, sentence_length = 50):
    texts = []
    num = 0
    fileList = os.listdir(pathname)
    os.chdir(pathname)
    for filename in fileList:
        if filename.endswith(".json"):
            file = open(filename, "r")
            data = json.load(file)
            texts.append(data['text'][:sentence_length].lower())
            num += 1
            if(num > numLimit and numLimit != -1):
                return texts
    return texts

if __name__ == '__main__':
    data = loadData('./technology/',5)
    print(data)