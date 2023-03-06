import pandas as pd

from service import division_plus_list, get_new_flag_dont_work_сount_cam, division_plus_list_plus_num_cam, \
    get_new_flag_work_geo_on_cam, get_new_flag_work_сount_cam


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



