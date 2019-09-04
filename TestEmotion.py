import Stemmer
import os
import pickle
import re
import numpy as np
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.text import text_to_word_sequence
from keras.preprocessing.sequence import pad_sequences
from keras.preprocessing import sequence
from keras.models import load_model

#MAX_LENGTH = 26
#CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

def preprocess_text(text):
    text = text.lower().replace("ё", "е")                               #Замена Ё на Е
    text = re.sub('((www\.[^\s]+)|(https?://[^\s]+))', 'URL', text)     #Замена ссылок на токен «URL»
    text = re.sub('@[^\s]+', 'USER', text)                              #Замена упоминания пользователя на токен «USER»
    text = re.sub('[^a-zA-Zа-яА-Я1-9]+', ' ', text)                     #Удаление знаков пунктуации
    text = re.sub(' +', ' ', text)
    return text.strip()

def Stemming (stemmer, str1):
    worldsList = text_to_word_sequence(str1)
    tempData = stemmer.stemWords(worldsList)
    return (" ".join(tempData))

def TextPreparation (tokenizer, SENTENCE_LENGTH, text):
    stemmer = Stemmer.Stemmer('russian')
    str = preprocess_text(text)
    str = Stemming(stemmer, str)
    data = list()
    data.append(str)
    sequences = tokenizer.texts_to_sequences(data)
    return pad_sequences(sequences, maxlen=SENTENCE_LENGTH)

class ToneClassifier:
    MAX_LENGTH = 26
    CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

    model = load_model(CURRENT_DIR + '/my_trained_model/Trained_model.h5')
    t = Tokenizer()

    def __init__(self):
        with open(self.CURRENT_DIR + '/data/tokenizer.pickle', 'rb') as handle:
            self.t = pickle.load(handle)

    def analyse(self, text):
        testdata = TextPreparation (self.t, self.MAX_LENGTH, text)
        result = self.model.predict(testdata)
        return result
        

#Загрузка токенизатора
# t = Tokenizer()
# with open(CURRENT_DIR + '/data/tokenizer.pickle', 'rb') as handle:
#     t = pickle.load(handle)

##########################################################
#Блок подготовки текста
# def preprocess_text(self, text):
#     text = text.lower().replace("ё", "е")                               #Замена Ё на Е
#     text = re.sub('((www\.[^\s]+)|(https?://[^\s]+))', 'URL', text)     #Замена ссылок на токен «URL»
#     text = re.sub('@[^\s]+', 'USER', text)                              #Замена упоминания пользователя на токен «USER»
#     text = re.sub('[^a-zA-Zа-яА-Я1-9]+', ' ', text)                     #Удаление знаков пунктуации
#     text = re.sub(' +', ' ', text)
#     return text.strip()

# def Stemming (stemmer, str1):
#     worldsList = text_to_word_sequence(str1)
#     tempData = stemmer.stemWords(worldsList)
#     return (" ".join(tempData))

# def TextPreparation (tokenizer, SENTENCE_LENGTH, str):
#     stemmer = Stemmer.Stemmer('russian')
#     str = preprocess_text(str)
#     str = Stemming(stemmer, str)
#     data = list()
#     data.append(str)
#     sequences = tokenizer.texts_to_sequences(data)
#     return pad_sequences(sequences, maxlen=SENTENCE_LENGTH)
#Конец блока подготовки текста
##########################################################################

#Загрузка модели
#model = load_model(CURRENT_DIR + '/my_trained_model/Trained_model.h5')

#Проверка модели
# teststring = "кино отстой, никому не рекомендую"
# testdata = TextPreparation (t, MAX_LENGTH, teststring)
# result = model.predict(testdata)
# print(result)
