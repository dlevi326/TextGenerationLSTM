
import loadData
from statistics import mean
import tensorflow as tf
import numpy as np

from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import LSTM
from keras.callbacks import ModelCheckpoint

# Sentence length in characters
SENT_LEN = 100 # Max and min doc length for x values
EPOCHS = 100
SEQ_LEN = 100 # Number of characters in sequences for x values
NUM_GEN_CHARS = 1000 # Number of characters to generate

data = loadData.loadData('./technology',100,sentence_length=SENT_LEN)

joinedData = ''.join(data)

new = ''
for i in joinedData:
	if i.isalpha() or i==' ':
		new+=i
joinedData = new
unique_chars = set(joinedData)
charMap = {}
charMapReverse = {}
for ind,char in enumerate(unique_chars):
    charMap[char] = ind
    charMapReverse[ind] = char
print(charMapReverse)

# Sanitizing data
x_data = []
y_data = []
for i in range(0,len(joinedData)-SEQ_LEN):
    prev_chars = joinedData[i:i+SEQ_LEN]
    next_char = joinedData[i+SEQ_LEN]
    #print(prev_chars,'--',next_char)
    x_data.append([charMap[l] for l in prev_chars])
    y_data.append(charMap[next_char])


# Reshaping - LSTM needs form of [samples,time steps, features]
x_data_new = np.reshape(x_data,(len(x_data),SEQ_LEN,1))

# Normalize
x_data_new = x_data_new/len(unique_chars)

# One-hot the y data
y_data = tf.keras.utils.to_categorical(y_data)


# Train Model

model = Sequential()
model.add(LSTM(256, input_shape=(x_data_new.shape[1], x_data_new.shape[2]), return_sequences=True))
model.add(LSTM(256))
model.add(Dropout(0.2))
model.add(Dense(y_data.shape[1], activation='softmax'))
model.compile(loss='categorical_crossentropy', optimizer='adam')
model.fit(x_data_new, y_data, epochs=EPOCHS, batch_size=128)


beginning_code = np.random.randint(0,len(x_data)-1)
charString = x_data[beginning_code]
print("Seed:")
print([charMapReverse[val] for val in charString])

# Generate characters
for i in range(NUM_GEN_CHARS):
	x = np.reshape(charString, (1, len(charString), 1))
	x = x / float(len(unique_chars))
	prediction = model.predict(x, verbose=0)
	index = np.argmax(prediction)
	result = charMapReverse[index]
	print(result,end='')
	charString.append(index)
	charString = charString[1:]
print("\nDone.")






