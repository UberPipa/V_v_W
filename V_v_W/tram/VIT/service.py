import numpy as np
import pandas as pd

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



