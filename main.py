
import loadData
from statistics import mean

# Sentence length in characters
SENT_LEN = 50

data = loadData.loadData('./technology',10)


lens = []
for i in data:
    lens.append(len(i))
print(mean(lens))




