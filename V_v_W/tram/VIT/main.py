import pandas as pd
from datetime import date

from openpyxl.utils import get_column_letter

from logic import get_df_full_bad_cam, get_without_remont, get_df_partly_bad_cam, get_df_full_and_partly_bad_cam, \
    get_df_partly_without_geo_cam, get_df_full_without_geo_cam, get_df_full_available_cam, \
    get_df_full_and_partly_without_geo_cam, get_df_full_available_and_partly_bad_cam
from process_input_data import read_remont, create_df
from work_and_print_module import work
pd.options.mode.chained_assignment = None #Выключает предупреждения

work()



# inputDate = '2023-02-06'
# #1, 2 process_input_data
# df_cam, vl_df_cam, tv_df_cam, df_tram, vl_df_tram, tv_df_tram, count_tram, count_vl_tram, count_tv_tram, list_tram, vl_list_tram, tv_list_tram = create_df() # Читаем и делаем df, распаковываем
# df_remont_cam, vl_df_remont_cam , tv_df_remont_cam, df_remont_tram, vl_df_remont_tram, tv_df_remont_tram, count_remont_tram, count_vl_remont_tram, count_tv_remont_tram, list_remont_tram, vl_list_remont_tram, tv_list_remont_tram = read_remont(df_cam) # Считывает и хранит ремонтные составы
# #3 get_without_remont
# df_without_remont_cam, vl_df_without_remont_cam, tv_df_without_remont_cam, df_without_remont_tram, vl_df_without_remont_tram, tv_df_without_remont_tram, count_without_remont_tram, count_vl_without_remont_tram, count_tv_without_remont_tram, list_without_remont_tram, vl_list_without_remont_tram, tv_list_without_remont_tram = get_without_remont(df_cam, df_remont_cam)
# #4 get_df_full_and_partly_bad_cam
# df_full_and_partly_bad_cam, vl_df_full_and_partly_bad_cam, tv_df_full_and_partly_bad_cam, df_full_and_partly_bad_tram, vl_df_full_and_partly_bad_tram, tv_df_full_and_partly_bad_tram, count_full_and_partly_bad_tram, count_vl_full_and_partly_bad_tram, count_tv_full_and_partly_bad_tram, list_full_and_partly_bad_tram, list_vl_full_and_partly_bad_tram, list_tv_full_and_partly_bad_tram = get_df_full_and_partly_bad_cam(df_without_remont_cam, inputDate)
# #5 get_df_full_bad_cam
# df_full_bad_cam, vl_df_full_bad_cam, tv_df_full_bad_cam, df_full_bad_tram, vl_df_full_bad_tram, tv_df_bad_tram, count_full_bad_tram, count_vl_full_bad_tram, count_tv_full_bad_tram, list_full_bad_tram, list_vl_full_bad_tram, list_tv_full_bad_tram = get_df_full_bad_cam(df_full_and_partly_bad_cam)
# #6 get_df_partly_bad_cam
# df_partly_bad_cam, vl_df_partly_bad_cam, tv_df_partly_bad_cam, df_partly_bad_tram, vl_df_partly_bad_tram, tv_df_partly_bad_tram, count_partly_bad_tram, count_vl_partly_bad_tram, count_tv_partly_bad_tram, list_partly_bad_tram, list_vl_partly_bad_tram, list_tv_partly_bad_tram = get_df_partly_bad_cam(df_full_and_partly_bad_cam, df_cam)
# #7 get_df_full_available_and_partly_bad_cam - Доступные
# df_full_available_and_partly_bad_cam, df_vl_full_available_and_partly_bad_cam, df_tv_full_available_and_partly_bad_cam, full_available_and_partly_bad_tram, vl_full_available_and_partly_bad_tram, tv_full_available_and_partly_bad_tram, count_full_available_and_partly_bad_tram, count_vl_full_available_and_partly_bad_tram, count_tv_full_available_and_partly_bad_tram, list_full_available_and_partly_bad_tram, list_vl_full_available_and_partly_bad_tram, list_tv_full_available_and_partly_bad_tram = get_df_full_available_and_partly_bad_cam(df_without_remont_cam, df_full_bad_cam, inputDate)
# #8 get_df_full_and_partly_without_geo_cam
# df_full_and_partly_without_geo_cam, vl_df_full_and_partly_without_geo_cam, tv_df_full_and_partly_without_geo_cam, df_full_and_partly_without_geo_tram, vl_df_full_and_partly_without_geo_tram, tv_df_full_and_partly_without_geo_tram, count_full_and_partly_without_geo_tram, vl_count_full_and_partly_without_geo_tram, tv_count_full_and_partly_without_geo_tram, list_full_and_partly_without_geo_tram, vl_list_full_and_partly_without_geo_tram, tv_list_full_and_partly_without_geo_tram = get_df_full_and_partly_without_geo_cam(df_full_available_and_partly_bad_cam)
# #9 get_df_full_without_geo_cam
# df_full_without_geo_cam, vl_df_full_without_geo_cam, tv_df_full_without_geo_cam, df_full_without_geo_tram, vl_df_full_without_geo_tram, tv_df_full_without_geo_tram, count_full_without_geo_tram, count_vl_full_without_geo_tram, count_tv_full_without_geo_tram, list_full_without_geo_tram, list_vl_full_without_geo_tram, list_tv_full_without_geo_tram = get_df_full_without_geo_cam(df_full_and_partly_without_geo_cam)
# #10 get_df_partly_without_geo_cam
# df_partly_without_geo_cam, vl_df_partly_without_geo_cam, tv_df_partly_without_geo_cam, df_partly_without_geo_tram, vl_df_partly_without_geo_tram, tv_df_partly_without_geo_tram, count_df_partly_without_geo_tram, count_vl_df_partly_without_geo_tram, count_tv_df_partly_without_geo_tram, list_df_partly_without_geo_tram, list_vl_df_partly_without_geo_tram, list_tv_df_partly_without_geo_tram = get_df_partly_without_geo_cam(df_full_and_partly_without_geo_cam)
# #11 get_df_full_available_cam
# df_full_available_cam, df_vl_full_available_cam, df_tv_full_available_cam, df_full_available_tram, df_vl_full_available_tram, df_tv_full_available_tram, count_full_available_tram, count_vl_full_available_tram, count_tv_full_available_tram, list_full_available_tram, list_vl_full_available_tram, list_tv_full_available_tram = get_df_full_available_cam(df_full_available_and_partly_bad_cam, df_full_without_geo_cam)
#
#
#
#
#
# # Всё для Exel
# current_date = date.today()
#
# result_cam = pd.concat([df_remont_cam, df_full_available_cam, df_partly_bad_cam, df_full_bad_cam, df_full_without_geo_cam]) # Дружим все дф
# result_cam = result_cam.sort_values(by=['N_sostava', 'N_camera']) # Сортировка
# result_cam = result_cam[['N_sostava', 'vendor', 'status', 'N_camera', 'status_cam', 'SYS_last_time_check_on_camera', 'dont_work_geo_on_cam', 'SYS_last_lat_on_camera', 'SYS_last_lon_on_camera', 'сount_cam', 'work_сount_cam']] # Правильно располагаем и избавляемся от лишнего
# result_cam.rename(columns={'N_sostava': '№ трамвая', 'vendor': 'Вендор', 'status': 'Статус трамвая', 'status_cam': 'Статус камеры', 'SYS_last_time_check_on_camera': 'Последняя детекция', 'dont_work_geo_on_cam': 'Cтатус геопозиции', 'SYS_last_lat_on_camera': 'Широта', 'SYS_last_lon_on_camera': 'Долгота', 'N_camera': '№ камеры', 'сount_cam': 'Камер на трамвае', 'work_сount_cam': 'Камер работает'},inplace=True)  # Переименования для excel
#
#
# result_tram = pd.concat([df_remont_tram, df_full_available_tram, df_partly_bad_tram, df_full_bad_tram, df_full_without_geo_tram]) # Дружим все дф
# result_tram = result_tram.sort_values(by=['N_sostava']) # Сортировка
# result_tram = result_tram[['N_sostava', 'vendor', 'status', 'SYS_last_time_check_on_camera', 'dont_work_geo_on_cam', 'SYS_last_lat_on_camera', 'SYS_last_lon_on_camera', 'сount_cam', 'work_сount_cam']]
# result_tram.rename(columns={'N_sostava': '№ трамвая', 'vendor': 'Вендор', 'status': 'Статус трамвая', 'SYS_last_time_check_on_camera': 'Последняя детекция трамвая', 'dont_work_geo_on_cam': 'Cтатус геопозиции', 'SYS_last_lat_on_camera': 'Широта', 'SYS_last_lon_on_camera': 'Долгота', 'сount_cam': 'Камер на трамвае', 'work_сount_cam': 'Камер работают'},inplace=True)  # Переименования для excel
#
#
# with pd.ExcelWriter(f'output_data/{current_date} - Статистика по камерам.xlsx') as writer:
#     result_tram.to_excel(writer, sheet_name="Статистика по трамваям", index=False) # Записываем
#     workbook = writer.book # Определяем док
#     worksheet = writer.sheets['Статистика по трамваям'] # Находим лист
#     worksheet.autofilter(0, 0, result_tram.shape[0], result_tram.shape[1] - 1) # фильтр
#     result_cam.to_excel(writer, sheet_name="Статистика по камерам", index=False)
#     worksheet = writer.sheets['Статистика по камерам'] # Находим лист
#     worksheet.autofilter(0, 0, result_cam.shape[0], result_cam.shape[1] - 1) # фильтр
#     for i in writer.sheets.keys():
#         writer.sheets[i].autofit()
#
#
# def ggg(df):
#     with pd.option_context('display.max_rows', None, 'display.max_columns', None, 'display.width', None):
#           print(df)
#     print(df.nunique())
#     print(str(len(df)) + ' Длинна')
# ggg(result_tram)





