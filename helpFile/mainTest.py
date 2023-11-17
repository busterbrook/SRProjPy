import speech_recognition as sr

r = sr.Recognizer()
audio_file = sr.AudioFile('testttt.flac')

with audio_file as source:
    audio = r.record(source)

text = r.recognize_sphinx(audio)

print(text)