from django.shortcuts import render
# Create your views here.

def index(request):

    data = {
        'title': 'Главная страницa',
        'values': ['Menu', 'Categories', 'Traceback'],

        'obj': {
            'car': 'bmw',
            'age': 18,
            'hobby': 'football',
        }
    }

    return render(request, 'main/index.html',  data)

def about(request):
    return render(request, 'main/about.html')