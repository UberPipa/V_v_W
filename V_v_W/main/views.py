from django.shortcuts import render
from django.core.cache import cache


# Create your views here.
def index(request):
    return render(request, 'main/index.html')

def about(request):
    return render(request, 'main/about.html')

def reports(request):
    if request.method == 'POST':
        birthday = request.POST.get('birthday')

        print(birthday)



    return render(request, 'main/reports.html', {'data': birthday})



