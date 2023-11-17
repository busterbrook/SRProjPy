#Все функции программы
from vosk import Model, KaldiRecognizer, SetLogLevel
from pydub import AudioSegment
from datetime import datetime
import librosa as l
import pandas as pd
import os
import subprocess
import json
import time
import random

SetLogLevel(0)

#Функция разделения большого аудио на части
def chunk_audio(audio_path, len, parts):

    sound = AudioSegment.from_mp3(audio_path)
    startTime = 0
    endTime = 0 + (len/parts) * 1000
    chunks = []

    for i in range(1,parts + 1):
        extract = sound[startTime:endTime]
        chunkFileName = audio_path + str(i) + '-extract.mp3'
        extract.export(chunkFileName, format="mp3")
        #chunks.append(chunkFileName)
        startTime += parts*60*1000
        endTime += parts*60*1000
        print("Создан файл " + chunkFileName)
        #time.sleep(random.randint(1,10))

    os.remove(audio_path)
    print("Удален файл " + chunkFileName)
    #return chunks
    
#Функция пороверки длительности файлов 
def check_len_file(path_name):
    arr_exit = []
    for filename in os.listdir(path_name):
        if filename.endswith('.mp3'):
            if (l.get_duration(filename = os.path.join(path_name, filename)))/60 > 10:
                arr_exit.append(filename)
    return arr_exit

#Транскрибация
def audToText(aud_name):
    current_time = datetime.now()
    print("Начало обработки", aud_name, str(current_time))
    # Проверяем наличие модели
    if not os.path.exists("vosk-model-small-ru-0.22"):
        print ("Please download the model from https://alphacephei.com/vosk/models and unpack as 'model' in the current folder.")
        exit (1)

    # Устанавливаем Frame Rate
    FRAME_RATE = 16000
    CHANNELS=1
    print("1 - Устанавливаем Frame Rate для файла", aud_name)

    model = Model("vosk-model-small-ru-0.22")
    rec = KaldiRecognizer(model, FRAME_RATE)
    rec.SetWords(True)
    print("2 - Устновка модели для файла", aud_name)

    # Используя библиотеку pydub делаем предобработку аудио
    mp3 = AudioSegment.from_mp3(aud_name)
    mp3 = mp3.set_channels(CHANNELS)
    mp3 = mp3.set_frame_rate(FRAME_RATE)
    print("3 - Обработка аудио для файла", aud_name)

    # Преобразуем вывод в json
    #time.sleep(random.randint(1,10))
    rec.AcceptWaveform(mp3.raw_data)
    result = rec.Result()
    text = result[result.rfind(':')+3:result.rfind('"')]
    #text = json.loads(result)["text"]
    print("4 - Преобразуем вывод в json для файла", aud_name)
    print("Время обработки файла", aud_name, str(datetime.now() - current_time))
    #print(text)

    # Добавляем пунктуацию
    #cased = subprocess.check_output('python3 recasepunc/recasepunc.py predict recasepunc/checkpoint', shell=True, text=True, input=text)
    #print("5 - Добавляем пунктуацию")

    # Записываем результат в файл "data.txt"
    #with open('data.txt', 'w') as f:
        #json.dump(text, f, ensure_ascii=False, indent=4)
    #print("6 - Записываем результат в файл data")

    return text

#Проверка наличия ключевых слов
def check_words(arr_text, key_words):
    res_arr = []
    for word in arr_text:
        if word in key_words:
            res_arr.append(word)
    return res_arr

#Чтение ключевых слов из файла 
def from_txt_to_list():
    with open("key_words.txt", "r") as file:
        key_words = file.read()
    return key_words