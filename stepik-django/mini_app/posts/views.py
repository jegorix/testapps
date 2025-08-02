from django.shortcuts import render
from datetime import datetime
from .forms import UserForm, PersonForm, ProfileForm, UserFormAdd, SortForm
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound, HttpResponsePermanentRedirect
from .models import Person, User
from django.forms.models import model_to_dict
# Create your views here.

# def index(request):
#     goods = Product.objects.all()
#     return render(request=request, template_name="index.html", context={"goods": goods})

# def index(request):
#     people = Worker.objects.all().order_by("-age")
#     # Worker.objects.create(first_name="Ted", last_name="Barinov", age=34, created=datetime.now(), work_experience=5)
#     # people = Worker.objects.all().order_by("-age").filter(first_name="Ted").exclude(last_name="Ivanov")
#     # goods = Product.objects.all().order_by("-price")
#     goods = Product.objects.all().order_by("?")
#     # item = Product.objects.filter(name="MacBook").get()
#     # item = Product.objects.filter(id=5).values().get()
#     item = Worker.objects.filter(first_name="Ted").all().values_list("first_name", "last_name")
    
    
#     if request.method == "POST":
#         userform = UserForm(request.POST)
#         if userform.is_valid():
#             name = userform.cleaned_data["name"]
#             return HttpResponse(f'<h2>Hello, {name}</h2>')
#     else:
#         userform = UserForm()
    
    
#     return render(request=request, template_name="posts/index.html",
#                   context={"people": people,
#                            "goods": goods,
#                            "item": item,
#                            "form": userform})



def index(request):
    people = Person.objects.all()
    form = PersonForm()
    return render(request=request, template_name="posts/index.html", context={"people": people, "form": form})


def create(request):
    if request.method == "POST":
        form = PersonForm(request.POST)
        if form.is_valid():
            form.save()
    return HttpResponseRedirect("/")



def edit(request, id):
    try:
        person = Person.objects.get(id=id)
        
        if request.method == "POST":
            form = PersonForm(request.POST, instance=person)
            if form.is_valid():
                form.save()
            return HttpResponseRedirect("/")
        
        else:
            form = PersonForm(instance=person)
            return render(request=request, template_name="posts/edit.html", context={'form': form})
            
    except Person.DoesNotExist:
        return HttpResponseNotFound('<h2>Person not found</h2>')
    


def delete(request, id):
    try:
        person = Person.objects.get(id=id)
        person.delete()
        return HttpResponseRedirect("/")
    
    except Person.DoesNotExist:
        return HttpResponseNotFound('<h2>Person not found</h2>')
    
    
    
    

def user_profile(request):
    users = User.objects.all()
    return render(request=request, template_name="posts/user_list.html", context={"users": users})

def add_user(request):
    if request.method == "POST":
        form = UserFormAdd(request.POST)
        if form.is_valid():
            form.save()
        return HttpResponsePermanentRedirect("/user/")
    
    else:
        form = UserFormAdd()
        return render(request=request, template_name="posts/user_profile.html", context={"form": form})
        
            
def delete_profile(request, id):
    try:
        user = User.objects.get(id=id)
        user.delete()
        return HttpResponsePermanentRedirect("/user/")
    
    except User.DoesNotExist:
        return HttpResponseNotFound(f"<h2>User profile with id={id} not found</h2>.")
    
    
def edit_profile(request, id):
    try:
        user = User.objects.get(id=id)
        
        if request.method == "POST":
            form = UserFormAdd(request.POST, instance=user)
            
            if form.is_valid():
                form.save()
            return HttpResponsePermanentRedirect("/user/")
            
        
        form = UserFormAdd(instance=user)
        return render(request=request, template_name="posts/edit_user.html", context={"form": form})
    
    except User.DoesNotExist:
        return HttpResponseNotFound(f"<h2>User profile with id={id} not found</h2>.")
    
    
def sort_users(request):
    
    users = User.objects.all()
    
    sort_field = request.GET.get("sort_field", "id")
    sort_direction = request.GET.get("sort_direction", "asc")
    
    if sort_direction == 'desc':
        sort_param = f'-{sort_field}'
    else:
        sort_param = sort_field
        
    users = users.order_by(sort_param)
    
    form = SortForm(initial={
        'sort_field': sort_field,
        "sort_direction": sort_direction
    })
    
  
    return render(request=request, template_name="posts/sort_users.html", context={
                "form": form,
                "users": users,
                "sort_field": sort_field,
                "sort_direction": sort_direction
            })
        