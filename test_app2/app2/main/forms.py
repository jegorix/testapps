from .models import Tasks
from django.forms import ModelForm, TextInput, Textarea, DateInput, CheckboxInput, RadioSelect

class TasksForm(ModelForm):
    class Meta:
        model = Tasks
        fields = ['title', 'description', 'deadline', 'priority', 'is_done']
        widgets = {
            'title': TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Task Title',
            }),

            'description':  Textarea(attrs={
                'class': 'form-input',
                'placeholder': 'Task Description',
                'rows': 4,
            }),

            'deadline': DateInput(attrs={
                'class': 'form-input',
                'placeholder': 'Deadline',
                'type': 'date',
            }),

            'priority': RadioSelect(attrs={
                'class': 'form-radio-group'
            }),

            'is_done': CheckboxInput(attrs={
                'class': 'form-check-input',
            }),

        }

