# Determine Note model for working with DB
from django.db import models
from django.core.validators import MaxLengthValidator
# Create your models here.

class Note(models.Model):
    title = models.CharField(max_length=200,
                             verbose_name='Заголовок',
                             help_text='Введите заголовок заметки')
    
    content = models.TextField(validators=[MaxLengthValidator(10000)],
                               verbose_name='Содержание',
                               help_text='Введите содержание заметки')
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания',
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления'
    )
    
    class Meta:
        verbose_name = 'Заметка'
        verbose_name_plural = 'Заметки'
        ordering = ['-created_at']
        
    def __str__(self) -> str:
        return self.title[:50]