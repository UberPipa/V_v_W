from django.shortcuts import render

from .models import act_data


# Create your views here.
def index(request):
    return render(request, 'main/index.html')

def about(request):
    return render(request, 'main/about.html')

def reports(request):
    if request.method == 'POST':
        birthday = request.POST.get('birthday')
        birthday = act_data(data = birthday)
        birthday.save()

    return render(request, 'main/reports.html')



