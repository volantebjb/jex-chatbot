import json
import pickle
import random
import numpy
from nltk.stem import LancasterStemmer
from nltk import download
from tensorflow.keras.layers import Dense
from tensorflow.keras.models import Sequential, model_from_yaml
from textblob import TextBlob

nltk.download('punkt')

stemmer = LancasterStemmer()

with open("intents.json") as file:
    data = json.load(file)

try:
    with open("chatbot.pickle", "rb") as file:
        words, labels, training, output = pickle.load(file)

except Exception as e:
    print(f"An error occurred: {e}")
    words = []
    labels = []
    docs_x = []
    docs_y = []

    for intent in data["intents"]:
        for pattern in intent["patterns"]:
            wrds = nltk.word_tokenize(pattern)
            words.extend(wrds)
            docs_x.append(wrds)
            docs_y.append(intent["tag"])

        if intent["tag"] not in labels:
            labels.append(intent["tag"])

    words = [stemmer.stem(w.lower()) for w in words if w != "?"]
    words = sorted(list(set(words)))

    labels = sorted(labels)

    training = []
    output = []

    output_empty = [0 for _ in range(len(labels))]

    for x, doc in enumerate(docs_x):
        bag = []

        wrds = [stemmer.stem(w.lower()) for w in doc]

        for w in words:
            if w in wrds:
                bag.append(1)
            else:
                bag.append(0)

        output_row = output_empty[:]
        output_row[labels.index(docs_y[x])] = 1

        training.append(bag)
        output.append(output_row)

    training = numpy.array(training)
    output = numpy.array(output)

    with open("chatbot.pickle", "wb") as file:
        pickle.dump((words, labels, training, output), file)

try:
    yaml_file = open('chatbotmodel.yaml', 'r')
    loaded_model_yaml = yaml_file.read()
    yaml_file.close()
    myChatModel = model_from_yaml(loaded_model_yaml)
    myChatModel.load_weights("chatbotmodel.h5")
    print("Loaded model from disk")

except:
    myChatModel = Sequential()
    myChatModel.add(Dense(8, input_shape=[len(words)], activation='relu'))
    myChatModel.add(Dense(len(labels), activation='softmax'))
    myChatModel.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    myChatModel.fit(training, output, epochs=1000, batch_size=8)

    model_yaml = myChatModel.to_yaml()
    with open("chatbotmodel.yaml", "w") as y_file:
        y_file.write(model_yaml)

    myChatModel.save_weights("chatbotmodel.h5")
    print("Saved model from disk")

def bag_of_words(s, words):
    bag = [0 for _ in range(len(words))]

    s_words = nltk.word_tokenize(s)
    s_words = [stemmer.stem(word.lower()) for word in s_words]

    for se in s_words:
        for i, w in enumerate(words):
            if w == se:
                bag[i] = 1

    return numpy.array(bag)

# Errors

universal_errors = [
        'Sorry, hindi kita naiintindihan.', 
        'Parang may mali.',
        'Ano ang nais mong sabihin?',
        'Paumanhin, hindi ko mawari ang iyong tinutukoy.'
    ]

soft_errors = [
        'Hindi ito ang inaasahan kong sagot.'
        ]

# Prints

def primary(inputText):
    currentText = bag_of_words(inputText, words)
    currentTextArray = [currentText]
    numpyCurrentText = numpy.array(currentTextArray)

    if numpy.all((numpyCurrentText == 0)):
        return random.choice(universal_errors)

    result = myChatModel.predict(numpyCurrentText[0:1])
    result_index = numpy.argmax(result)
    tag = labels[result_index]

    if result[0][result_index] > 0.7:
        for tg in data["intents"]:
            if tg['tag'] == tag:
                responses = tg['responses']
                return random.choice(responses)                
                    
        else:
            return random.choice(soft_errors)

    else:
        return random.choice(universal_errors)
    
def secondary(inputText):
    
    if primary(inputText) != universal_errors or soft_errors:
        currentText = bag_of_words(inputText, words)
        currentTextArray = [currentText]
        numpyCurrentText = numpy.array(currentTextArray)
        result = myChatModel.predict(numpyCurrentText[0:1])
        result_index = numpy.argmax(result)
        tag = labels[result_index]

        if result[0][result_index] > 0.7:
            for tg in data["intents"]:
                if tg['tag'] == tag:
                    followup = tg['followup']
                    return random.choice(followup)
                
# Sentiment Analysis

def sa(inputText):

    blob = TextBlob(inputText)
    print('Polarity: ',blob.polarity)

def chat():
    print("Start talking with the chatbot (try quit to stop)")

    while True:
        inp = input("You: ")
        if inp.lower() == "quit":
            break

        print(primary(inp))
        print(sa(inp))
        
chat()
