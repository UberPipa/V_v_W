#from datetime import *
import datetime
from V_v_W.main.views import act_data


def date_check():
    # Вводим начальную дату
    #inputDate = input('Введите дату от которой будут проверяться трамваи в формате YYYY-MM-DD: ')
    inputDate = act_data
    print(inputDate)
    formate = "%Y-%m-%d" # Проверяем формат даты
    res = True
    try:
        res = bool(datetime.datetime.strptime(inputDate, formate))
    except ValueError:
        res = False
    # Выдаём результат
    if res == True:
        print("Дата выбрана! Вы выбрали - " + inputDate)
        start_date = inputDate
    else:
        print("Введена не корректная дата!")
        date_check()
    data_start = datetime.datetime.strptime(inputDate, '%Y-%m-%d') # из строки в дату
    data_end = data_start + datetime.timedelta(days=6) # Прибавляем 6 дней
    data_start = str(data_start.strftime('%Y-%m-%d')) # В строку
    data_end = str(data_end.strftime('%Y-%m-%d')) # В строку
    return str(inputDate), data_start, data_end
