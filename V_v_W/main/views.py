from django.shortcuts import render
import tempfile


# Create your views here.
def index(request):
    return render(request, 'main/index.html')

def about(request):
    return render(request, 'main/about.html')

act_data = {}
def reports(request):
    global act_data
    if request.method == 'POST':
        birthday = request.POST.get('birthday')
        act_data = {'birthday': birthday}

        print(dict(act_data))

    return render(request, 'main/reports.html', {'daterange': birthday})


