from librosa import get_duration
import math
from controller import *

if __name__ == '__main__':

    path_name = "audio"
    res_arr_list = {}

    dff = pd.DataFrame()
    dff.to_excel("output123.xlsx")

    keys = from_txt_to_list().split()
    print("Чтение ключевых слов из файла")

    res =  check_len_file(path_name)
    if res:
        for filename in res:
            len = int(get_duration(filename=os.path.join(path_name, filename)))
            parts = int(math.ceil(len/60/15))
            chunks = chunk_audio(os.path.join(path_name, filename), len, parts)
            print(chunks)
            print("Файлы приведены к обработке")

    for filename in os.listdir(path_name):
        df = pd.DataFrame()
        if filename.endswith('.mp3'):
            enter_file_name = os.path.join(path_name, filename)
            arr_text = check_words(audToText(enter_file_name).split(),keys)
            df.insert(loc=0, column = 'Key_Word', value = arr_text)
            df1 = df.groupby(['Key_Word'])['Key_Word'].count()
            print(df1)
            with pd.ExcelWriter('output123.xlsx',mode='a') as writer:  
                df1.to_excel(writer, sheet_name=filename)
            #res_arr_list[filename] = arr_text
    print("DONE")

"""
    print(res_arr_list)
    df.insert(loc=0, column = 'Key_Word', value = res)
    df1 = df.groupby(['Key_Word'])['Key_Word'].count()
    df1.to_excel("output.xlsx")
    print(df1)

    with pd.ExcelWriter('output.xlsx') as writer:  
        df1.to_excel(writer, sheet_name='Sheet_name_1')
        df2.to_excel(writer, sheet_name='Sheet_name_2')

    res = check_words(arr_text, keys)


 
    aud_name = 'audio/s' + '.mp3' #названиве аудио файла + формат файла

   
    arr_text = audToText(aud_name).split()

  

    df = pd.DataFrame()
    df.insert(loc=0, column = 'Key_Word', value = res)
    df1 = df.groupby(['Key_Word'])['Key_Word'].count()
    df1.to_excel("output.xlsx")
    print(df1)
    """