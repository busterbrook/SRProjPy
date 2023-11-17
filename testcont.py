from librosa import get_duration
import math
from controller import *

if __name__ == '__main__':

    path_name = "audio"
    res_arr_list = {}

    dff = pd.DataFrame()
    dff.to_excel("output.xlsx")

    keys = from_txt_to_list().split()
    print("Чтение ключевых слов из файла")

    res = check_len_file(path_name)
    if res:
        for filename in res:
            len = int(get_duration(filename=os.path.join(path_name, filename)))
            parts = int(math.ceil(len/60/10))
            chunk_audio(os.path.join(path_name, filename), len, parts)
            #chunks = chunk_audio(os.path.join(path_name, filename), len, parts)
            #print(chunks)
            print("Файлы приведены к обработке")

    for filename in os.listdir(path_name):
        df = pd.DataFrame()
        if filename.endswith('.mp3'):
            enter_file_name = os.path.join(path_name, filename)
            arr_text = check_words(audToText(enter_file_name).split(),keys)
            df.insert(loc=0, column = 'Key_Word', value = arr_text)
            df1 = df.groupby(['Key_Word'])['Key_Word'].count()
            print(df1)
            with pd.ExcelWriter('output.xlsx',mode='a') as writer:  
                df1.to_excel(writer, sheet_name=filename)

    print("DONE")
