from django.shortcuts import render
from django.views.generic import CreateView

# Create your views here.

def create(request):
    return render(request, 'main/create.html')

def show(request):
    return render(request, 'main/create.html')

