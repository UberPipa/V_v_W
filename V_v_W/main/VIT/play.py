import os
import sys
import pandas as pd
import numpy as np
import datetime

from pandas import read_csv

pd.options.mode.chained_assignment = None #Выключает предупреждения


def float_to_int(df, col): # меняет float на int с округлением в меньшую сторону, вставляет nan
    df[col] = df[col].apply(np.floor)  # Округляем в меньшую сторону
    df[col] = pd.to_numeric(df[col], errors='coerce').astype('Int64')
    #df[col] = pd.to_numeric(df[col].round(), errors='coerce').astype('Int64') # старый способ
    df[col] = df[col].replace({0: np.nan})
    df[col] = df[col].replace({90: np.nan})
    df[col] = df[col].replace({-90: np.nan})

def clean_df(df): # Очищает список и возвращает его и его длинну в 2 переменные
    clean_df = df.drop_duplicates(subset=["N_sostava"], keep='last') # удаляем дубликаты и не нужные столбцы
    count_df = len(clean_df) # Получаем длинну этого df
    return clean_df, count_df

def get_str_list_tram(df_tram):  # Получение строки с трамваями
    df_tram = list(df_tram['N_sostava'])  # Делаем список с составами
    df_tram = list(str(i) for i in df_tram)  # Делаем строку
    str_tram = ', '.join(df_tram)  # Делаем строку
    return str_tram

def division_plus_list(df): # Функция принимает один df любого множества _cam, после чего парсит на 12 переменных, возвращает начальный. Затем делит каждую переменную по вендорам
    df_tram = df.sort_values(by='last_time_check_on_camera', na_position='first')  # Сортировка на нахождения последней детекции
    df_tram = df_tram.drop_duplicates(subset=["N_sostava"], keep='last') # удаляем дубликаты и не нужные столбцы
    df_tram = df_tram.sort_values(by=['N_sostava', 'N_camera'])  # Сортировка
    df_tram.pop('N_camera')  # удаляет не нужный столбец
    df_tram.pop('last_time_check_on_camera')  # удаляет не нужный столбец
    df_tram.pop('last_lat_on_camera')  # удаляет не нужный столбец
    df_tram.pop('last_lon_on_camera')  # удаляет не нужный столбец
    count_tram = len(df_tram) # Получаем длинну этого df
    vl_df_cam = df[(df['vendor'] == 'vl')]  # Все составы vl
    tv_df_cam = df[(df['vendor'] == 'tv')]  # Все составы vt
    vl_df_tram = df_tram[(df_tram['vendor'] == 'vl')]  # Все составы vl
    tv_df_tram = df_tram[(df_tram['vendor'] == 'tv')]  # Все составы tv
    count_vl_tram = len(vl_df_tram)  # Получаем длинну этого df
    count_tv_tram = len(tv_df_tram)  # Получаем длинну этого df
    list_tram = get_str_list_tram(df_tram) # Получаем строку
    vl_list_tram = get_str_list_tram(vl_df_tram) # Получаем строку
    tv_list_tram = get_str_list_tram(tv_df_tram) # Получаем строку
    return df, vl_df_cam, tv_df_cam, df_tram, vl_df_tram, tv_df_tram, count_tram, count_vl_tram, count_tv_tram, list_tram, vl_list_tram, tv_list_tram

def get_new_flag_dont_work_сount_cam(df): # Делает флаги не работающих камер
    df['dont_work_сount_cam'] = df.groupby('N_sostava')['N_sostava'].transform('size')  # Присваивает новые флаги с реальным количеством камер
    return df

def get_new_flag_work_сount_cam(df): # Делает флаги не работающих камер
    df['work_сount_cam'] = df.groupby('N_sostava')['N_sostava'].transform('size')  # Присваивает новые флаги с реальным количеством камер
    return df

def get_new_flag_work_geo_on_cam(df): # Делает флаги
    df['dont_work_geo_on_cam'] = df.groupby('N_sostava')['N_sostava'].transform('size')  # Присваивает новые флаги с реальным количеством камер
    return df

def col_in_str_plus_cam(df_cam, df_tram): # Возвращает строку составов c номерами камер
    df_tram = list(df_tram['N_sostava'])  # Делаем список с составами
    all_sost = []  # список для всех составов
    for item in df_tram:  # шагаем по списку с составами
        for sost in df_cam['N_sostava']:  # шагаем по списку
            if sost == item:
                index = df_cam.index[df_cam.N_sostava == sost]  # Получаем индекс
                index = index.tolist()  # оборачиваем в лист
                list_cam = []  # временный список для хранения камер
                for i in index:  # находим по индексу номера камер
                    cam = df_cam.loc[i, 'N_camera']  # находим по индексу номера камер
                    list_cam.append(str(cam))  # добавляем в список камеры поочерёдно
                list_cam = ','.join(list_cam)  # делаем строку для вывода для каждого списка камер
                each_sost = f'{sost}({list_cam})'  # переменная для строки со всеми составами
                all_sost.append(each_sost)  # добавляем каждый состав в список
    temp = []  # временный спиоск
    [temp.append(x) for x in all_sost if x not in temp]  # удаляем дубликаты списка
    temp = ', '.join(temp)  # делаем строку
    all_sost = temp  # присваиваем
    return all_sost

def division_plus_list_plus_num_cam(df, df_for_ls): # Функция принимает один df любого множества _cam, после чего парсит на 12 переменных, возвращает начальный. Затем делит каждую переменную по вендорам
    df_tram = df.sort_values(by='last_time_check_on_camera', na_position='first')  # Сортировка на нахождения последней детекции
    df_tram = df_tram.drop_duplicates(subset=["N_sostava"], keep='last') # удаляем дубликаты и не нужные столбцы
    df_tram = df_tram.sort_values(by=['N_sostava', 'N_camera'])  # Сортировка
    df_tram.pop('N_camera')  # удаляет не нужный столбец
    df_tram.pop('last_time_check_on_camera')  # удаляет не нужный столбец
    df_tram.pop('last_lat_on_camera')  # удаляет не нужный столбец
    df_tram.pop('last_lon_on_camera')  # удаляет не нужный столбец
    count_tram = len(df_tram) # Получаем длинну этого df
    vl_df_cam = df_for_ls[(df_for_ls['vendor'] == 'vl')]  # Все составы vl
    tv_df_cam = df_for_ls[(df_for_ls['vendor'] == 'tv')]  # Все составы vt
    vl_df_tram = df_tram[(df_tram['vendor'] == 'vl')]  # Все составы vl
    tv_df_tram = df_tram[(df_tram['vendor'] == 'tv')]  # Все составы tv
    count_vl_tram = len(vl_df_tram)  # Получаем длинну этого df
    count_tv_tram = len(tv_df_tram)  # Получаем длинну этого df
    list_tram = col_in_str_plus_cam(df_for_ls, df_tram) # Получаем строку
    vl_list_tram = col_in_str_plus_cam(vl_df_cam, vl_df_tram) # Получаем строку
    tv_list_tram = col_in_str_plus_cam(tv_df_cam, tv_df_tram) # Получаем строку
    return df, vl_df_cam, tv_df_cam, df_tram, vl_df_tram, tv_df_tram, count_tram, count_vl_tram, count_tv_tram, list_tram, vl_list_tram, tv_list_tram


def date_check(inputDate):

    import datetime
    # Вводим начальную дату
    #inputDate = input('Введите дату от которой будут проверяться трамваи в формате YYYY-MM-DD: ')
    #inputDate = '2023-01-03'

    # formate = "%Y-%m-%d" # Проверяем формат даты
    # res = True
    # try:
    #     res = bool(datetime.datetime.strptime(inputDate, formate))
    # except ValueError:
    #     res = False
    # # Выдаём результат
    # if res == True:
    #     #print("Дата выбрана! Вы выбрали - " + inputDate)
    #     start_date = inputDate
    # else:
    #     print("Введена не корректная дата!")
    #     date_check(inputDate)



    data_start = datetime.datetime.strptime(inputDate, '%Y-%m-%d') # из строки в дату
    data_end = data_start + datetime.timedelta(days=6) # Прибавляем 6 дней
    data_start = str(data_start.strftime('%Y-%m-%d')) # В строку
    data_end = str(data_end.strftime('%Y-%m-%d')) # В строку
    return str(inputDate), data_start, data_end


def create_df():  #1 читает из CVS, создаёт df и форматирует его
    cwd = os.getcwd() + '\\main\\VIT'
    name_df = read_csv(f"{cwd}\\input_data\\input_cam.txt") # Читаем
    df = pd.DataFrame(name_df) # Помещаем в переменную
    df.drop(df[df['status'] == '-'].index, inplace=True) # Удаляет архивные
    df.pop('status')  # удаляет не нужный столбец
    df.pop('num_composition')  # удаляет не нужный столбец
    #df.pop('split_part')  # удаляет не нужный столбец
    df.pop('vendor')  # удаляет не нужный столбец
    df['vendor'] = df.camera.str.split('_').str[0] # Парсим
    df['N_sostava'] = df.camera.str.split('_').str[4] # Парсим
    df['N_camera'] = df.camera.str.split('_').str[5]  # Парсим
    df['SYS_last_time_check_on_camera'] = df['last_time_check_on_camera'] # Служебный для Excel
    df['SYS_last_lat_on_camera'] = df['last_lat_on_camera']  # Служебный для Excel
    df['SYS_last_lon_on_camera'] = df['last_lon_on_camera']  # Служебный для Excel
    df['status'] = ''  # Служебный для Excel
    df['last_time_check_on_camera'] = pd.to_datetime(df['last_time_check_on_camera'])  # Переделывает в datetime
    df['last_time_check_on_camera'] = df['last_time_check_on_camera'].dt.ceil('T') # Ибавляемся от миллисекунд в last_time_check_on_camera
    df["N_sostava"] = df["N_sostava"].astype(int) # меняем на str на int
    df["N_camera"] = df["N_camera"].astype(int) # меняем на str на int
    float_to_int(df, "last_lat_on_camera") # меняет float на int с округлением в меньшую сторону, вставляет nan
    float_to_int(df, "last_lon_on_camera") # меняет float на int с округлением в меньшую сторону, вставляет nan
    df['сount_cam'] = df.groupby('N_sostava')['N_sostava'].transform('size')  # Делаем флаг с количесвом камер для cоставов с количесвом камер для каждого состава
    df = df[['vendor', 'N_sostava', 'N_camera', 'last_time_check_on_camera', 'last_lat_on_camera', 'last_lon_on_camera','сount_cam', 'SYS_last_time_check_on_camera', 'SYS_last_lat_on_camera', 'SYS_last_lon_on_camera', 'status']]  # упорядочеваем столбцы
    df = df.sort_values(by=['N_sostava', 'N_camera'])  # Двойная сортировка массива по N_sostava затем N_camera
    df_cam, vl_df_cam, tv_df_cam, df_tram, vl_df_tram, tv_df_tram, count_tram, count_vl_tram, count_tv_tram, list_tram, vl_list_tram, tv_list_tram = division_plus_list(df)  # # Функция принимает один df любого множества _cam, после чего распараллеливает на 9 переменных, возвращает начальный df_cam, df_tram и  count_tram. Затем делит каждую переменную по вендорам
    return df_cam, vl_df_cam, tv_df_cam, df_tram, vl_df_tram, tv_df_tram, count_tram, count_vl_tram, count_tv_tram, list_tram, vl_list_tram, tv_list_tram

def read_remont(df_cam): #2 Читает и возвращает список ремонтных составов с вендорами
    cwd = os.getcwd() + '\\main\\VIT'
    list_remont_cam = read_csv(f"{cwd}\\input_data\\remont.txt", names=['N_sostava'], header=None) # Читаем
    df_remont_cam = pd.DataFrame(list_remont_cam) # Создаём
    df_remont_cam = df_cam[(df_cam['N_sostava'].isin(df_remont_cam['N_sostava'])) == True] # оставляем только ремнтники
    df_remont_cam['status'] = 'Трамвай в ремонте' # Служебный для Excel
    #df_remont_cam['work_сount_cam'] = 'Трамвай в ремонте'  # Служебный для Excel
    #df_remont_cam['dont_work_сount_cam'] = 'Трамвай в ремонте'  # Служебный для Excel
    #df_remont_cam['dont_work_geo_on_cam'] = 'Трамвай в ремонте' # Добавляем статус камеры
    #df_remont_cam['status_cam'] = 'Трамвай в ремонте'  # Добавляем статус камеры
    df_remont_cam, vl_df_remont_cam , vl_df_remont_cam, df_remont_tram, vl_df_remont_tram, tv_df_remont_tram, count_remont_tram, count_vl_remont_tram, count_tv_remont_tram, list_remont_tram, vl_list_remont_tram, tv_list_remont_tram  = division_plus_list(df_remont_cam) # распаковываем
    return df_remont_cam, vl_df_remont_cam , vl_df_remont_cam, df_remont_tram, vl_df_remont_tram, tv_df_remont_tram, count_remont_tram, count_vl_remont_tram, count_tv_remont_tram, list_remont_tram, vl_list_remont_tram, tv_list_remont_tram


def get_without_remont(df_cam, df_remont_cam): #3 получение трамваев без ремонта
    df_without_remont_cam = df_cam[(df_cam['N_sostava'].isin(df_remont_cam['N_sostava'])) == False]  # Хранит все составы без ремонтных, удаляет ремонтные и зазбивает по вендорам
    df_without_remont_cam, vl_df_without_remont_cam, tv_df_without_remont_cam, df_without_remont_tram, vl_df_without_remont_tram, tv_df_without_remont_tram, count_without_remont_tram, count_vl_without_remont_tram, count_tv_without_remont_tram, list_without_remont_tram, vl_list_without_remont_tram, tv_list_without_remont_tram = division_plus_list(df_without_remont_cam)
    return df_without_remont_cam, vl_df_without_remont_cam, tv_df_without_remont_cam, df_without_remont_tram, vl_df_without_remont_tram, tv_df_without_remont_tram, count_without_remont_tram, count_vl_without_remont_tram, count_tv_without_remont_tram, list_without_remont_tram, vl_list_without_remont_tram, tv_list_without_remont_tram

def get_df_full_and_partly_bad_cam(df_without_remont_cam, inputDate): #4 Получение частично и полностью без детекций. _cam получает только камеры, не трамваи!!!
    df_full_and_partly_bad_cam = df_without_remont_cam[(df_without_remont_cam['last_time_check_on_camera'].isnull()) | (df_without_remont_cam['last_time_check_on_camera'] < inputDate)]
    df_full_and_partly_bad_cam = get_new_flag_dont_work_сount_cam(df_full_and_partly_bad_cam)  # Делает флаги для последующих вычистений
    df_full_and_partly_bad_cam, vl_df_full_and_partly_bad_cam, tv_df_full_and_partly_bad_cam, df_full_and_partly_bad_tram, vl_df_full_and_partly_bad_tram, tv_df_full_and_partly_bad_tram, count_full_and_partly_bad_tram, count_vl_full_and_partly_bad_tram, count_tv_full_and_partly_bad_tram, list_full_and_partly_bad_tram, list_vl_full_and_partly_bad_tram, list_tv_full_and_partly_bad_tram = division_plus_list(df_full_and_partly_bad_cam)
    return df_full_and_partly_bad_cam, vl_df_full_and_partly_bad_cam, tv_df_full_and_partly_bad_cam, df_full_and_partly_bad_tram, vl_df_full_and_partly_bad_tram, tv_df_full_and_partly_bad_tram, count_full_and_partly_bad_tram, count_vl_full_and_partly_bad_tram, count_tv_full_and_partly_bad_tram, list_full_and_partly_bad_tram, list_vl_full_and_partly_bad_tram, list_tv_full_and_partly_bad_tram
def get_df_full_bad_cam(df_full_and_partly_bad_cam): #5 Получение полностью без детекций. _cam!!!
    df_full_bad_cam = df_full_and_partly_bad_cam.loc[df_full_and_partly_bad_cam['сount_cam'] == df_full_and_partly_bad_cam['dont_work_сount_cam']] # Сравнивает флаги
    df_full_bad_cam['status'] = 'Полностью не доступен'  # Служебный для Excel
    df_full_bad_cam['status_cam'] = 'Камера не доступна' # Добавляем статус камеры
    df_full_bad_cam['work_сount_cam'] = df_full_bad_cam['сount_cam'] - df_full_bad_cam['dont_work_сount_cam']  # Определяем количесвто работающих камер
    df_full_bad_cam['dont_work_geo_on_cam'] = 'Геопозиция трамвая не определена'
    df_full_bad_cam, vl_df_full_bad_cam, tv_df_full_bad_cam, df_full_bad_tram, vl_df_full_bad_tram, tv_df_bad_tram, count_full_bad_tram, count_vl_full_bad_tram, count_tv_full_bad_tram, list_full_bad_tram, list_vl_full_bad_tram, list_tv_full_bad_tram = division_plus_list(df_full_bad_cam)
    return df_full_bad_cam, vl_df_full_bad_cam, tv_df_full_bad_cam, df_full_bad_tram, vl_df_full_bad_tram, tv_df_bad_tram, count_full_bad_tram, count_vl_full_bad_tram, count_tv_full_bad_tram, list_full_bad_tram, list_vl_full_bad_tram, list_tv_full_bad_tram

def get_df_partly_bad_cam(df_full_and_partly_bad_cam, df_cam): #6 Получение частично без детекций. _cam получает только камеры, не трамваи!!!
    df_partly_bad_cam = df_full_and_partly_bad_cam.loc[df_full_and_partly_bad_cam['сount_cam'] != df_full_and_partly_bad_cam['dont_work_сount_cam']] # Получили частично не доступные, но имеются только часть камер на них
    df_partly_bad_cam['work_сount_cam'] = df_partly_bad_cam['сount_cam'] - df_partly_bad_cam['dont_work_сount_cam']  # Определяем количесвто не работающих камер
    df_for_ls = df_partly_bad_cam
    df_partly_bad_cam['status_cam'] = 'Камера не доступна' # Добавляем статус камеры
    temp3 = df_partly_bad_cam.drop_duplicates(subset=['N_sostava'])[['N_sostava','dont_work_сount_cam', 'work_сount_cam']] # дф с Составом и коунтом
    temp = df_cam[(df_cam['N_sostava'].isin(df_partly_bad_cam['N_sostava']))] # Возвращаем все _cam в соответсвивии с составами, они были удалены при сортировке
    temp2 = temp[~(temp.index.isin(df_partly_bad_cam.index))] # Камеры, которых не хватает
    temp2['status_cam'] = 'Камера доступна'
    df_partly_bad_cam = pd.concat([df_partly_bad_cam, temp2]) # Складываем изначальные и которых не хватает
    df_partly_bad_cam = df_partly_bad_cam.sort_values(by=['N_sostava', 'N_camera']) # Сортировка
    df_partly_bad_cam = pd.merge(df_partly_bad_cam.drop(['dont_work_сount_cam', 'work_сount_cam'], axis = 1), temp3, how='left', on='N_sostava' ).set_index(df_partly_bad_cam.index) # Джоиним DF + Удаляем лишние столбцы
    df_partly_bad_cam['status'] = 'Частично не доступен' # Служебный для Excel
    df_partly_bad_cam['dont_work_geo_on_cam'] = 'Геопозиция трамвая определена'
    df_partly_bad_cam, vl_df_partly_bad_cam, tv_df_partly_bad_cam, df_partly_bad_tram, vl_df_partly_bad_tram, tv_df_partly_bad_tram, count_partly_bad_tram, count_vl_partly_bad_tram, count_tv_partly_bad_tram, list_partly_bad_tram, list_vl_partly_bad_tram, list_tv_partly_bad_tram = division_plus_list_plus_num_cam(df_partly_bad_cam, df_for_ls)
    return df_partly_bad_cam, vl_df_partly_bad_cam, tv_df_partly_bad_cam, df_partly_bad_tram, vl_df_partly_bad_tram, tv_df_partly_bad_tram, count_partly_bad_tram, count_vl_partly_bad_tram, count_tv_partly_bad_tram, list_partly_bad_tram, list_vl_partly_bad_tram, list_tv_partly_bad_tram

def get_df_full_available_and_partly_bad_cam(df_without_remont_cam, df_full_bad_cam, inputDate): #7 Все доступные
    df_full_available_and_partly_bad_cam = df_without_remont_cam[~(df_without_remont_cam['N_sostava'].isin(df_full_bad_cam['N_sostava']))]# Ищем доступные Все
    df_full_available_and_partly_bad_cam = df_full_available_and_partly_bad_cam[(df_full_available_and_partly_bad_cam['last_time_check_on_camera'] > inputDate)] # по дате, отсеиваем не доступные _cam
    df_full_available_and_partly_bad_cam, df_vl_full_available_and_partly_bad_cam, df_tv_full_available_and_partly_bad_cam, full_available_and_partly_bad_tram, vl_full_available_and_partly_bad_tram, tv_full_available_and_partly_bad_tram, count_full_available_and_partly_bad_tram, count_vl_full_available_and_partly_bad_tram, count_tv_full_available_and_partly_bad_tram, list_full_available_and_partly_bad_tram, list_vl_full_available_and_partly_bad_tram, list_tv_full_available_and_partly_bad_tram = division_plus_list(df_full_available_and_partly_bad_cam)
    return df_full_available_and_partly_bad_cam, df_vl_full_available_and_partly_bad_cam, df_tv_full_available_and_partly_bad_cam, full_available_and_partly_bad_tram, vl_full_available_and_partly_bad_tram, tv_full_available_and_partly_bad_tram, count_full_available_and_partly_bad_tram, count_vl_full_available_and_partly_bad_tram, count_tv_full_available_and_partly_bad_tram, list_full_available_and_partly_bad_tram, list_vl_full_available_and_partly_bad_tram, list_tv_full_available_and_partly_bad_tram

def get_df_full_and_partly_without_geo_cam(df_full_available_and_partly_bad_cam): # Без гео данных
    df_full_and_partly_without_geo_cam = df_full_available_and_partly_bad_cam[(df_full_available_and_partly_bad_cam['last_lat_on_camera'].isnull()) | (df_full_available_and_partly_bad_cam['last_lon_on_camera'].isnull())]  # Находим трамваи без гео данных
    df_full_and_partly_without_geo_cam, vl_df_full_and_partly_without_geo_cam, tv_df_full_and_partly_without_geo_cam, df_full_and_partly_without_geo_tram, vl_df_full_and_partly_without_geo_tram, tv_df_full_and_partly_without_geo_tram, count_full_and_partly_without_geo_tram, vl_count_full_and_partly_without_geo_tram, tv_count_full_and_partly_without_geo_tram, list_full_and_partly_without_geo_tram, vl_list_full_and_partly_without_geo_tram, tv_list_full_and_partly_without_geo_tram = division_plus_list(df_full_and_partly_without_geo_cam)
    df_full_and_partly_without_geo_cam = get_new_flag_work_geo_on_cam(df_full_and_partly_without_geo_cam) # Флаг для последующх расчётов
    return df_full_and_partly_without_geo_cam, vl_df_full_and_partly_without_geo_cam, tv_df_full_and_partly_without_geo_cam, df_full_and_partly_without_geo_tram, vl_df_full_and_partly_without_geo_tram, tv_df_full_and_partly_without_geo_tram, count_full_and_partly_without_geo_tram, vl_count_full_and_partly_without_geo_tram, tv_count_full_and_partly_without_geo_tram, list_full_and_partly_without_geo_tram, vl_list_full_and_partly_without_geo_tram, tv_list_full_and_partly_without_geo_tram

def get_df_full_without_geo_cam(df_full_and_partly_without_geo_cam): #9 Полностью без гео данных
    df_full_without_geo_cam = df_full_and_partly_without_geo_cam.loc[df_full_and_partly_without_geo_cam['сount_cam'] == df_full_and_partly_without_geo_cam['dont_work_geo_on_cam']] # Сравнивает флаги
    df_full_without_geo_cam['status'] = 'Геопозиция отсутствует'  # Служебный для Excel
    df_full_without_geo_cam['dont_work_сount_cam'] = 0
    df_full_without_geo_cam['work_сount_cam'] = 6
    df_full_without_geo_cam['dont_work_geo_on_cam'] = 'Геопозиция трамвая не определена'
    df_full_without_geo_cam['status_cam'] = 'Камера доступна'
    df_full_without_geo_cam, vl_df_full_without_geo_cam, tv_df_full_without_geo_cam, df_full_without_geo_tram, vl_df_full_without_geo_tram, tv_df_full_without_geo_tram, count_full_without_geo_tram, count_vl_full_without_geo_tram, count_tv_full_without_geo_tram, list_full_without_geo_tram, list_vl_full_without_geo_tram, list_tv_full_without_geo_tram = division_plus_list(df_full_without_geo_cam)
    return df_full_without_geo_cam, vl_df_full_without_geo_cam, tv_df_full_without_geo_cam, df_full_without_geo_tram, vl_df_full_without_geo_tram, tv_df_full_without_geo_tram, count_full_without_geo_tram, count_vl_full_without_geo_tram, count_tv_full_without_geo_tram, list_full_without_geo_tram, list_vl_full_without_geo_tram, list_tv_full_without_geo_tram

def get_df_partly_without_geo_cam(df_full_and_partly_without_geo_cam): #10 Частично без гео данных
    df_partly_without_geo_cam = df_full_and_partly_without_geo_cam.loc[df_full_and_partly_without_geo_cam['сount_cam'] != df_full_and_partly_without_geo_cam['dont_work_geo_on_cam']]  # Сравнивает флаги
    df_partly_without_geo_cam, vl_df_partly_without_geo_cam, tv_df_partly_without_geo_cam, df_partly_without_geo_tram, vl_df_partly_without_geo_tram, tv_df_partly_without_geo_tram, count_df_partly_without_geo_tram, count_vl_df_partly_without_geo_tram, count_tv_df_partly_without_geo_tram, list_df_partly_without_geo_tram, list_vl_df_partly_without_geo_tram, list_tv_df_partly_without_geo_tram = division_plus_list_plus_num_cam(df_partly_without_geo_cam, df_partly_without_geo_cam)
    return df_partly_without_geo_cam, vl_df_partly_without_geo_cam, tv_df_partly_without_geo_cam, df_partly_without_geo_tram, vl_df_partly_without_geo_tram, tv_df_partly_without_geo_tram, count_df_partly_without_geo_tram, count_vl_df_partly_without_geo_tram, count_tv_df_partly_without_geo_tram, list_df_partly_without_geo_tram, list_vl_df_partly_without_geo_tram, list_tv_df_partly_without_geo_tram

def get_df_full_available_cam(df_full_available_and_partly_bad_cam, df_full_and_partly_without_geo_cam):
    temp = get_new_flag_work_сount_cam(df_full_available_and_partly_bad_cam)  # Делает флаги для последующих вычистений
    temp = temp.loc[temp['сount_cam'] == temp['work_сount_cam']] # Сравнивает флаги
    df_full_available_cam = temp[~(temp['N_sostava'].isin(df_full_and_partly_without_geo_cam['N_sostava']))]# удаляем все трамваи без гео данных
    df_full_available_cam['dont_work_сount_cam'] = df_full_available_cam['сount_cam'] - df_full_available_cam['work_сount_cam'] # Определяем количесвто не работающих камер
    df_full_available_cam['status'] = 'Полностью доступен' # Служебный для Excel
    df_full_available_cam['status_cam'] = 'Камера доступна'
    df_full_available_cam['dont_work_geo_on_cam'] = 'Геопозиция трамвая определена'
    df_full_available_cam, df_vl_full_available_cam, df_tv_full_available_cam, df_full_available_tram, df_vl_full_available_tram, df_tv_full_available_tram, count_full_available_tram, count_vl_full_available_tram, count_tv_full_available_tram, list_full_available_tram, list_vl_full_available_tram, list_tv_full_available_tram = division_plus_list(df_full_available_cam)
    return df_full_available_cam, df_vl_full_available_cam, df_tv_full_available_cam, df_full_available_tram, df_vl_full_available_tram, df_tv_full_available_tram, count_full_available_tram, count_vl_full_available_tram, count_tv_full_available_tram, list_full_available_tram, list_vl_full_available_tram, list_tv_full_available_tram

# Порядок нахождения
# df_cam - Все                                                       #1
# 	df_remont_cam - Ремонтные                                        #2
# 	df_without_remont_cam - df без ремонтных                         #3
# 	df_full_and_partly_bad_cam - Частично и полностью без детекций   #4
# 		df_full_bad_cam - Полностью без детекций (Не доступные)      #5
# 		df_partly_bad_cam – Частично без детекций                    #6
# 	df_full_available_and_partly_bad_cam – Доступные                 #7
# 		df_partly_bad_cam - Частично без детекций                    #6
# 		df_full_available_cam - Полностью доступные                  #11
# 	df_full_and_partly_without_geo_cam – Без геоданных               #8
# 		df_full_without_geo_cam – Полностью без гео данных           #9
# 		df_partly_without_geo_cam – Частично без гео данных          #10


def work(inputDate):
    current_date = datetime.date.today()  # Текущая дата
    inputDate, data_start, data_end = date_check(inputDate)
    #1, 2 process_input_data
    df_cam, vl_df_cam, tv_df_cam, df_tram, vl_df_tram, tv_df_tram, count_tram, count_vl_tram, count_tv_tram, list_tram, vl_list_tram, tv_list_tram = create_df() # Читаем и делаем df, распаковываем
    df_remont_cam, vl_df_remont_cam , tv_df_remont_cam, df_remont_tram, vl_df_remont_tram, tv_df_remont_tram, count_remont_tram, count_vl_remont_tram, count_tv_remont_tram, list_remont_tram, vl_list_remont_tram, tv_list_remont_tram = read_remont(df_cam) # Считывает и хранит ремонтные составы
    #3 get_without_remont
    df_without_remont_cam, vl_df_without_remont_cam, tv_df_without_remont_cam, df_without_remont_tram, vl_df_without_remont_tram, tv_df_without_remont_tram, count_without_remont_tram, count_vl_without_remont_tram, count_tv_without_remont_tram, list_without_remont_tram, vl_list_without_remont_tram, tv_list_without_remont_tram = get_without_remont(df_cam, df_remont_cam)
    #4 get_df_full_and_partly_bad_cam
    df_full_and_partly_bad_cam, vl_df_full_and_partly_bad_cam, tv_df_full_and_partly_bad_cam, df_full_and_partly_bad_tram, vl_df_full_and_partly_bad_tram, tv_df_full_and_partly_bad_tram, count_full_and_partly_bad_tram, count_vl_full_and_partly_bad_tram, count_tv_full_and_partly_bad_tram, list_full_and_partly_bad_tram, list_vl_full_and_partly_bad_tram, list_tv_full_and_partly_bad_tram = get_df_full_and_partly_bad_cam(df_without_remont_cam, inputDate)
    #5 get_df_full_bad_cam
    df_full_bad_cam, vl_df_full_bad_cam, tv_df_full_bad_cam, df_full_bad_tram, vl_df_full_bad_tram, tv_df_bad_tram, count_full_bad_tram, count_vl_full_bad_tram, count_tv_full_bad_tram, list_full_bad_tram, list_vl_full_bad_tram, list_tv_full_bad_tram = get_df_full_bad_cam(df_full_and_partly_bad_cam)
    #6 get_df_partly_bad_cam
    df_partly_bad_cam, vl_df_partly_bad_cam, tv_df_partly_bad_cam, df_partly_bad_tram, vl_df_partly_bad_tram, tv_df_partly_bad_tram, count_partly_bad_tram, count_vl_partly_bad_tram, count_tv_partly_bad_tram, list_partly_bad_tram, list_vl_partly_bad_tram, list_tv_partly_bad_tram = get_df_partly_bad_cam(df_full_and_partly_bad_cam, df_cam)
    #7 get_df_full_available_and_partly_bad_cam - Доступные
    df_full_available_and_partly_bad_cam, df_vl_full_available_and_partly_bad_cam, df_tv_full_available_and_partly_bad_cam, full_available_and_partly_bad_tram, vl_full_available_and_partly_bad_tram, tv_full_available_and_partly_bad_tram, count_full_available_and_partly_bad_tram, count_vl_full_available_and_partly_bad_tram, count_tv_full_available_and_partly_bad_tram, list_full_available_and_partly_bad_tram, list_vl_full_available_and_partly_bad_tram, list_tv_full_available_and_partly_bad_tram = get_df_full_available_and_partly_bad_cam(df_without_remont_cam, df_full_bad_cam, inputDate)
    #8 get_df_full_and_partly_without_geo_cam
    df_full_and_partly_without_geo_cam, vl_df_full_and_partly_without_geo_cam, tv_df_full_and_partly_without_geo_cam, df_full_and_partly_without_geo_tram, vl_df_full_and_partly_without_geo_tram, tv_df_full_and_partly_without_geo_tram, count_full_and_partly_without_geo_tram, vl_count_full_and_partly_without_geo_tram, tv_count_full_and_partly_without_geo_tram, list_full_and_partly_without_geo_tram, vl_list_full_and_partly_without_geo_tram, tv_list_full_and_partly_without_geo_tram = get_df_full_and_partly_without_geo_cam(df_full_available_and_partly_bad_cam)
    #9 get_df_full_without_geo_cam
    df_full_without_geo_cam, vl_df_full_without_geo_cam, tv_df_full_without_geo_cam, df_full_without_geo_tram, vl_df_full_without_geo_tram, tv_df_full_without_geo_tram, count_full_without_geo_tram, count_vl_full_without_geo_tram, count_tv_full_without_geo_tram, list_full_without_geo_tram, list_vl_full_without_geo_tram, list_tv_full_without_geo_tram = get_df_full_without_geo_cam(df_full_and_partly_without_geo_cam)
    #10 get_df_partly_without_geo_cam
    df_partly_without_geo_cam, vl_df_partly_without_geo_cam, tv_df_partly_without_geo_cam, df_partly_without_geo_tram, vl_df_partly_without_geo_tram, tv_df_partly_without_geo_tram, count_df_partly_without_geo_tram, count_vl_df_partly_without_geo_tram, count_tv_df_partly_without_geo_tram, list_df_partly_without_geo_tram, list_vl_df_partly_without_geo_tram, list_tv_df_partly_without_geo_tram = get_df_partly_without_geo_cam(df_full_and_partly_without_geo_cam)
    #11 get_df_full_available_cam
    df_full_available_cam, df_vl_full_available_cam, df_tv_full_available_cam, df_full_available_tram, df_vl_full_available_tram, df_tv_full_available_tram, count_full_available_tram, count_vl_full_available_tram, count_tv_full_available_tram, list_full_available_tram, list_vl_full_available_tram, list_tv_full_available_tram = get_df_full_available_cam(df_full_available_and_partly_bad_cam, df_full_without_geo_cam)

    def opty_report():

        # l = [
        #     f'‼️Статистика по трамваям Витязь ({data_start} - {data_end}).',
        #     ' ',
        #     f'🔸Всего заведено в Сферу: {count_tram} шт.',
        #     f'🛠Находятся в ремонте: {count_remont_tram} шт.',
        #     ]
        # cwd = os.getcwd() + '\\main\\VIT'
        #
        # with open(f'{cwd}\\output_data\\example.txt', 'w', encoding="utf-8") as p:
        #     p.write('\n'.join(l))

        cwd = os.getcwd() + '\\main\\VIT'
        file_path = f'{cwd}\\output_data\\{current_date} - Отчёт по трамваям.txt' # Запись в файл в 2 страки
        sys.stdout = open(file_path, "w", encoding='utf-8') # Запись в файл в 2 страки
        print(f'‼️Статистика по трамваям Витязь ({data_start} - {data_end}).')
        print(' ')
        print(f'🔸Всего заведено в Сферу: {count_tram} шт.')
        print(f'🛠Находятся в ремонте: {count_remont_tram} шт.')
        print(f'❌Частично или полностью без детекций: {count_full_and_partly_bad_tram} шт.')
        print(f'✅Полностью рабочие трамваи: {count_full_available_tram} шт.')
        print(' ')
        print('‼️VisionLab')
        print(f'🔸Всего заведено в Сферу: {count_vl_tram} шт.')
        print(f'🛠Находятся в ремонте: {count_vl_remont_tram} шт.')
        print(f'❌Полностью не доступные трамваи: {count_vl_full_bad_tram} шт. : {list_vl_full_bad_tram}.')
        if count_vl_partly_bad_tram == 0:
            pass
        else:
            print(f'⚠️Трамваи, где не доступна часть камер : {count_vl_partly_bad_tram} шт. : {list_vl_partly_bad_tram}.')
        if count_vl_full_without_geo_tram == 0:
            pass
        else:
            print(f'⚠️Трамваи без геоданных: {count_vl_full_without_geo_tram} шт. : {list_vl_full_without_geo_tram}.')
        if count_vl_full_available_tram == 0:
            print(f'!!!Полностью рабочие ️трамваи отсутствуют!!!')
        else:
            print(f'✅Полностью рабочие ️трамваи: {count_vl_full_available_tram} шт.')
        print(' ')
        print('‼️Tevian')
        print(f'🔸Всего заведено в Сферу: {count_tv_tram} шт.')
        print(f'🛠Находятся в ремонте: {count_tv_remont_tram} шт.')
        print(f'❌Полностью не доступные ️трамваи: {count_tv_full_bad_tram} шт. : {list_tv_full_bad_tram}.')
        if count_tv_partly_bad_tram == 0:
            pass
        else:
            print(f'⚠️Трамваи, где не доступна часть камер : {count_tv_partly_bad_tram} шт. : {list_tv_partly_bad_tram}.')
        if count_tv_full_without_geo_tram == 0:
            pass
        else:
            print(f'⚠️Трамваи без геоданных: {count_tv_full_without_geo_tram} шт. : {list_tv_full_without_geo_tram}.')
        if count_tv_full_available_tram == 0:
            print(f'!!!Полностью рабочие ️трамваи отсутствуют!!!')
        else:
            print(f'✅Полностью рабочие ️трамваи: {count_tv_full_available_tram} шт.')

    def create_excel():
        result_cam = pd.concat([df_remont_cam, df_full_available_cam, df_partly_bad_cam, df_full_bad_cam,df_full_without_geo_cam])  # Дружим все дф
        result_cam = result_cam.sort_values(by=['N_sostava', 'N_camera'])  # Сортировка
        result_cam = result_cam[['N_sostava', 'vendor', 'status', 'N_camera', 'status_cam', 'SYS_last_time_check_on_camera','dont_work_geo_on_cam', 'SYS_last_lat_on_camera', 'SYS_last_lon_on_camera', 'сount_cam','work_сount_cam']]  # Правильно располагаем и избавляемся от лишнего
        result_cam.rename(columns={'N_sostava': '№ трамвая', 'vendor': 'Вендор', 'status': 'Статус трамвая','status_cam': 'Статус камеры', 'SYS_last_time_check_on_camera': 'Последняя детекция','dont_work_geo_on_cam': 'Cтатус геопозиции', 'SYS_last_lat_on_camera': 'Широта','SYS_last_lon_on_camera': 'Долгота', 'N_camera': '№ камеры','сount_cam': 'Камер на трамвае', 'work_сount_cam': 'Камер работает'},inplace=True)  # Переименования для excel
        result_tram = pd.concat([df_remont_tram, df_full_available_tram, df_partly_bad_tram, df_full_bad_tram,df_full_without_geo_tram])  # Дружим все дф
        result_tram = result_tram.sort_values(by=['N_sostava'])  # Сортировка
        result_tram = result_tram[['N_sostava', 'vendor', 'status', 'SYS_last_time_check_on_camera', 'dont_work_geo_on_cam','SYS_last_lat_on_camera', 'SYS_last_lon_on_camera', 'сount_cam', 'work_сount_cam']]
        result_tram.rename(columns={'N_sostava': '№ трамвая', 'vendor': 'Вендор', 'status': 'Статус трамвая','SYS_last_time_check_on_camera': 'Последняя детекция трамвая', 'dont_work_geo_on_cam': 'Cтатус геопозиции', 'SYS_last_lat_on_camera': 'Широта','SYS_last_lon_on_camera': 'Долгота', 'сount_cam': 'Камер на трамвае','work_сount_cam': 'Камер работают'}, inplace=True)  # Переименования для excel
        cwd = os.getcwd() + '\\main\\VIT'
        with pd.ExcelWriter(f'{cwd}\\output_data\\{current_date} - Статистика по трамваям.xlsx') as writer:
            result_tram.to_excel(writer, sheet_name="Статистика по трамваям", index=False)  # Записываем
            #workbook = writer.book  # Определяем док
            worksheet = writer.sheets['Статистика по трамваям']  # Находим лист
            worksheet.autofilter(0, 0, result_tram.shape[0], result_tram.shape[1] - 1)  # фильтр
            result_cam.to_excel(writer, sheet_name="Статистика по камерам", index=False)
            worksheet = writer.sheets['Статистика по камерам']  # Находим лист
            worksheet.autofilter(0, 0, result_cam.shape[0], result_cam.shape[1] - 1)  # фильтр
            for i in writer.sheets.keys():
                writer.sheets[i].autofit()
    opty_report()
    create_excel()
print('Готово')







