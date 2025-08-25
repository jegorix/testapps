from django.db import models
from django.core.validators import FileExtensionValidator
from django.contrib.auth.models import User
from mptt.models import MPTTModel, TreeForeignKey
from django.urls import reverse
from apps.services.utils import unique_slugify
# Create your models here.

class PostManager(models.Manager):
    """
    Кастомный менеджер для модели постов
    """
    def get_queryset(self):
        return super().get_queryset().select_related('author', 'category').filter(status="published")




class Post(models.Model):
    """
    Модель постов для нашего блога
    """
    
    objects = models.Manager()
    custom = PostManager()
    
    STATUS_OPTION = (
        ('published', 'Опубликовано'),
        ('draft', 'Черновик')
    )
    
    title = models.CharField(verbose_name='Название записи', max_length=255)
    slug = models.SlugField(verbose_name='URL', max_length=255, blank=True)
    description = models.TextField(verbose_name='Краткое описание', max_length=500)
    text = models.TextField(verbose_name='Полный текст записи')
    thumbnail = models.ImageField(default='default.jpg',
                                  verbose_name='Изображение записи',
                                  blank=True,
                                  upload_to='images/thumbnails/%Y/%m/%d',
                                  validators=[FileExtensionValidator(allowed_extensions=('png', 'jpg', 'webp', 'jpeg', 'gif'))]
                                  )
    status = models.CharField(choices=STATUS_OPTION,
                              default='published',
                              verbose_name='Статус записи',
                              max_length=10,
                              )
    create = models.DateTimeField(auto_now_add=True, verbose_name='Время добавления')
    update = models.DateTimeField(auto_now=True, verbose_name='Время обновления')
    
    author = models.ForeignKey(to=User, verbose_name='Автор', on_delete=models.SET_DEFAULT,
                               related_name='author_posts',
                               default=1)
    
    updater = models.ForeignKey(to=User, verbose_name='Обновил', on_delete=models.SET_NULL,
                                null=True, blank=True, related_name='updater_posts')
    
    fixed = models.BooleanField(verbose_name='Прикреплено', default=False)
    
    category = TreeForeignKey('Category', on_delete=models.CASCADE, related_name='posts', verbose_name="Категория")
    
    class Meta:
        db_table = 'blog_post'
        ordering = ['-fixed', '-create']
        indexes = [models.Index(fields=['-fixed', '-create', 'status'])]
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
        
    def __str__(self) -> str:
        return self.title
        
    def get_absolute_url(self):
        return reverse('post_detail', kwargs={"slug": self.slug})
    
    def save(self, *args, **kwargs):
        """
        При сохранении генерируем слаг и проверяем на уникальность
        """
        self.slug = unique_slugify(self, self.title)
        super().save(*args, **kwargs)        
    
        
        
        
class Category(MPTTModel):
    """
    Модель категорий с вложенностью
    """
    
    title = models.CharField(max_length=255, verbose_name="Название категории")
    slug = models.SlugField(max_length=255, verbose_name='URL категории', blank=True)
    description = models.TextField(verbose_name='Описание категории', max_length=300)
    parent = TreeForeignKey(
        'self',
        on_delete = models.CASCADE,
        null = True,
        blank = True,
        db_index = True,
        related_name = 'children',
        verbose_name = 'Родительская категория'
    )
    
    class MPTTMeta:
        """
        Сортировка по вложенности
        """
        order_insertion_by = ('title',)
        
    class Meta:
        """
        Сортировка, название модели в админ панели, таблица в данными
        """
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        db_table = 'app_categories'
        
    def __str__(self) -> str:
        """
        Возвращение заголовка категории
        """
        return self.title
    
    
    def get_absolute_url(self):
        return reverse("post_by_category", kwargs={"slug": self.slug})
    


class Comment(MPTTModel):
    """
    Модель древовидных комментариев
    """
    STATUS_OPTION = (
        ('pusblished', 'Опубликовано'),
        ('draft', 'Черновик')
        
    )
    
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='Запись', related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор комментария', related_name='comments_author')
    content = models.TextField(verbose_name='Текст комментария', max_length=3000)
    time_create = models.DateTimeField(verbose_name='Время создания', auto_now_add=True)
    time_update = models.DateTimeField(verbose_name='Время обновления', auto_now=True)
    status = models.CharField(choices=STATUS_OPTION, verbose_name='Статус поста', default='published', max_length=10)
    parent = TreeForeignKey('self', verbose_name='Родительский комментарий', null=True, blank=True,
                            related_name="children", on_delete=models.CASCADE)
    
    class MMTMeta:
        """
        Сортировка по вложенности
        """
        order_insertion_by=('-time_create', )
        
    class Meta:
        """
        Сортировка, название модели в админ панели, таблица в данными
        """
        ordering = ['-time_create']
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        
    def __str__(self):
        return f'{self.author}:{self.content}'
    
    