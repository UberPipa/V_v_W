import pandas as pd
from pandas import read_csv

from service import float_to_int, division_plus_list


def create_df():  #1 читает из CVS, создаёт df и форматирует его
    name_df = read_csv("input_data/input_cam.txt") # Читаем
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
    list_remont_cam = read_csv("input_data/remont.txt", names=['N_sostava'], header=None) # Читаем
    df_remont_cam = pd.DataFrame(list_remont_cam) # Создаём
    df_remont_cam = df_cam[(df_cam['N_sostava'].isin(df_remont_cam['N_sostava'])) == True] # оставляем только ремнтники
    df_remont_cam['status'] = 'Трамвай в ремонте' # Служебный для Excel
    #df_remont_cam['work_сount_cam'] = 'Трамвай в ремонте'  # Служебный для Excel
    #df_remont_cam['dont_work_сount_cam'] = 'Трамвай в ремонте'  # Служебный для Excel
    #df_remont_cam['dont_work_geo_on_cam'] = 'Трамвай в ремонте' # Добавляем статус камеры
    #df_remont_cam['status_cam'] = 'Трамвай в ремонте'  # Добавляем статус камеры
    df_remont_cam, vl_df_remont_cam , vl_df_remont_cam, df_remont_tram, vl_df_remont_tram, tv_df_remont_tram, count_remont_tram, count_vl_remont_tram, count_tv_remont_tram, list_remont_tram, vl_list_remont_tram, tv_list_remont_tram  = division_plus_list(df_remont_cam) # распаковываем
    return df_remont_cam, vl_df_remont_cam , vl_df_remont_cam, df_remont_tram, vl_df_remont_tram, tv_df_remont_tram, count_remont_tram, count_vl_remont_tram, count_tv_remont_tram, list_remont_tram, vl_list_remont_tram, tv_list_remont_tram