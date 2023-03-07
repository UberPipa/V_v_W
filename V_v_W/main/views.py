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
        # birthday = birthday.split('/')
        # birthday.reverse()
        # birthday = '-'.join(birthday)
        dat = act_data(current_data=birthday, id=0)
        dat.save()
    old_data = act_data.objects.all()
    return render(request, 'main/reports.html', {'old_data': old_data})

