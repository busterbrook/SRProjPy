from librosa import get_duration
import math
from controller import *

path_name = "audio"
res =  check_len_file(path_name)
len = int(get_duration(filename=os.path.join(path_name, 'big.mp3')))
parts = int(math.ceil(len/60/5))
print(len, " ---- ", parts)


"""print(res)
if res:
    for filename in res:
        len = int(get_duration(filename=os.path.join(path_name, filename)))
        parts = int(math.ceil(len/60/55))
        print(len, " ---- ", parts)
        break
        chunks = chunk_audio(os.path.join(path_name, filename), len, parts)
        print(chunks)"""
