from django.db import models
from django.utils import timezone

# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=50)
    company = models.CharField(max_length=30)
    price = models.IntegerField()
    
    
class Worker(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    age = models.SmallIntegerField(null=True)
    created = models.DateTimeField(default=timezone.now)
    work_experience = models.SmallIntegerField(default=0)


class Post(models.Model):
    text = models.TextField()
    
    def __str__(self) -> str:
        return self.text[:50]
    
# class Person(models.Model):
#     name = models.CharField(max_length=120)
#     content = models.TextField()
    
# class Category(models.Model):
#     name = models.CharField(max_length=50, verbose_name="Категории")
#     slug = models.SlugField(unique=True, verbose_name="Слаг - это часть URL-адреса ресурса")
    

# class Classroom(models.Model):
#     name = models.CharField(max_length=50)
#     code = models.CharField(max_length=11, unique=True)
#     description = models.TextField(null=True, default="")
#     created = models.DateTimeField(auto_now_add=True)
#     updated = models.DateTimeField(auto_now=True)
    
#     def __str__(self) -> str:
#         return self.name
    
    
# class Posts(models.Model):
#     title = models.CharField(max_length=255, verbose_name="Название записи")
#     slug = models.SlugField(max_length=80, unique=True, verbose_name="URL")
#     description = models.TextField(verbose_name="Краткое описание")
#     text = models.TextField(verbose_name="Полный текст записи")
#     created = models.DateTimeField(auto_now_add=True, verbose_name="Время добавления")
#     updated = models.DateTimeField(auto_now=True, verbose_name="Время обновления")
#     fixed = models.BooleanField(default=False, verbose_name="Прикреплено")
    
#     def __str__(self) -> str:
#         return self.title
    
#     class Meta:
#         ordering = ["-created"]
#         verbose_name = "Статья"
#         verbose_name_plural = "Статьи"
    
        