from vosk import Model, KaldiRecognizer, SetLogLevel
from pydub import AudioSegment
import pandas as pd
import subprocess
import json
import os

from controller import *

SetLogLevel(0)

def audToText(aud_name):
    # Проверяем наличие модели
    if not os.path.exists("vosk-model-small-ru-0.22"):
        print ("Please download the model from https://alphacephei.com/vosk/models and unpack as 'model' in the current folder.")
        exit (1)

    # Устанавливаем Frame Rate
    FRAME_RATE = 16000
    CHANNELS=1
    print("1 - Устанавливаем Frame Rate")

    model = Model("vosk-model-small-ru-0.22")
    rec = KaldiRecognizer(model, FRAME_RATE)
    rec.SetWords(True)
    print("2 - Устновка модели")

    # Используя библиотеку pydub делаем предобработку аудио
    mp3 = AudioSegment.from_mp3(aud_name)
    mp3 = mp3.set_channels(CHANNELS)
    mp3 = mp3.set_frame_rate(FRAME_RATE)
    print("3 - Обработка аудио")

    # Преобразуем вывод в json
    rec.AcceptWaveform(mp3.raw_data)
    result = rec.Result()
    text = json.loads(result)["text"]
    print("4 - Преобразуем вывод в json")
    #print(text)

    # Добавляем пунктуацию
    #cased = subprocess.check_output('python3 recasepunc/recasepunc.py predict recasepunc/checkpoint', shell=True, text=True, input=text)
    #print("5 - Добавляем пунктуацию")

    # Записываем результат в файл "data.txt"
    #with open('data.txt', 'w') as f:
        #json.dump(text, f, ensure_ascii=False, indent=4)
    #print("6 - Записываем результат в файл data")

    return text

def check_words(arr_text, key_words):
    res_arr = []
    for word in arr_text:
        if word in key_words:
            res_arr.append(word)
    return res_arr

def from_txt_to_list():
    with open("key_words.txt", "r") as file:
        key_words = file.read()
    return key_words

if __name__ == '__main__':
    aud_name = 'audio/s' + '.mp3' #названиве аудио файла + формат файла

    keys = from_txt_to_list().split()
    arr_text = audToText(aud_name).split()

    res = check_words(arr_text, keys)

    df = pd.DataFrame()
    df.insert(loc=0, column = 'Key_Word', value = res)
    df1 = df.groupby(['Key_Word'])['Key_Word'].count()
    df1.to_excel("output.xlsx")
    print(df1)

