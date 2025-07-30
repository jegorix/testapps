from django.shortcuts import render
from .models import Product, Worker
from datetime import datetime
from .forms import UserForm
from django.http import HttpResponse
# Create your views here.

# def index(request):
#     goods = Product.objects.all()
#     return render(request=request, template_name="index.html", context={"goods": goods})

def index(request):
    people = Worker.objects.all().order_by("-age")
    # Worker.objects.create(first_name="Ted", last_name="Barinov", age=34, created=datetime.now(), work_experience=5)
    # people = Worker.objects.all().order_by("-age").filter(first_name="Ted").exclude(last_name="Ivanov")
    # goods = Product.objects.all().order_by("-price")
    goods = Product.objects.all().order_by("?")
    # item = Product.objects.filter(name="MacBook").get()
    # item = Product.objects.filter(id=5).values().get()
    item = Worker.objects.filter(first_name="Ted").all().values_list("first_name", "last_name")
    
    
    if request.method == "POST":
        userform = UserForm(request.POST)
        if userform.is_valid():
            name = userform.cleaned_data["name"]
            return HttpResponse(f'<h2>Hello, {name}</h2>')
    else:
        userform = UserForm()
    
    
    return render(request=request, template_name="posts/index.html",
                  context={"people": people,
                           "goods": goods,
                           "item": item,
                           "form": userform})