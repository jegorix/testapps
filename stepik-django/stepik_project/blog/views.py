from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect

# Create your views here.

def index(request):
    return render(request, "blog/index.html", context={"data": "Index"})


def info(request):
    return render(request, "blog/info.html", context={"about": "О нас"})


def products(request, id):
    return HttpResponse(f"Товар {id}")


def comments(request, id):
    return HttpResponse(f"Комментарии о товаре {id}")


def questions(request, id):
    return HttpResponse(f"Вопросы о товаре {id}")

def user(request):
    age = request.GET.get("age")
    name = request.GET.get("name")
    return HttpResponse(f"<h2>Имя: {name}, Возраст: {age}</h2>")

def contacts(request):
    return HttpResponseRedirect("/user/")

def direct(request):
    return HttpResponsePermanentRedirect("/")



    
    