from django.shortcuts import render

from .models import act_data


# Create your views here.
def index(request):
    return render(request, 'main/index.html')


def about(request):
    return render(request, 'main/about.html')


# def reports(request):
#     if request.method == 'POST':
#         birthday = request.POST.get('birthday')
#         # birthday = birthday.split('/')
#         # birthday.reverse()
#         # birthday = '-'.join(birthday)
#         dat = act_data(current_data=birthday, id=0)
#         dat.save()
#     old_data = act_data.objects.all()
#     return render(request, 'main/reports.html', {'old_data': old_data})

def dataTime(request):
    if request.method == 'POST':
        print(request.POST)
        if 'birthday' in request.POST:  # Для получения даты
            birthday = request.POST.get('birthday')
            dat = act_data(current_data=birthday, id=0)
            dat.save()
        #elif request.POST.get('inDa') == 'run_function_calculate': # Для кнопки расчётов
        elif 'inDa' in request.POST:  # Для кнопки расчётов
            inputDate = act_data.objects.all()
            inputDate = str(inputDate[0])
            inputDate = inputDate.split('/')
            inputDate.reverse()
            inputDate = '-'.join(inputDate)
    old_data = act_data.objects.all()
    return render(request, 'main/reports.html', {'old_data': old_data})