from django.shortcuts import render
from .models import Tasks
from .forms import TasksForm
from django.contrib import messages
from django.views.generic import CreateView

# Create your views here.
#
class TaskCreateView(CreateView):
    model = Tasks
    template_name = 'main/create.html'
    form_class = TasksForm
    success_url = '/tmanager/show/'

    def form_valid(self, form):
        messages.success(self.request, 'Task Created!')
        return super().form_valid(form)


def show(request):
    return render(request, 'main/create.html')

