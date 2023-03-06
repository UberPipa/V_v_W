from django.shortcuts import render


# Create your views here.
def index(request):
    return render(request, 'main/index.html')

def about(request):
    return render(request, 'main/about.html')


act_data = {}
def reports(request):
    global act_data
    if request.method == 'POST':
        daterange = request.POST.get('daterange')
        act_data = {'daterange': daterange}
    return render(request, 'main/reports.html', {'daterange': daterange})


print(act_data)
