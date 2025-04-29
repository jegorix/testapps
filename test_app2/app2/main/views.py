from django.shortcuts import render, get_object_or_404, redirect
from .models import Tasks
from .forms import TasksForm
from django.contrib import messages
from django.views.generic import CreateView, ListView, UpdateView, DeleteView

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


class TasksListView(ListView):
    model = Tasks
    template_name = 'main/show.html'
    context_object_name = 'tasks'
    ordering = ['-deadline']


class TaskUpdateView(UpdateView):
    model = Tasks
    template_name = 'main/create.html'
    form_class = TasksForm
    success_url = '/tmanager/show/'


class TaskDeleteView(DeleteView):
    model = Tasks
    context_object_name = 'task'
    template_name = 'main/delete.html'
    success_url = '/tmanager/show/'


def show(request):
    return render(request, 'main/create.html')



