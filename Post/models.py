from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from .middleware import get_current_user
from django.db.models import Q


# модель Категорий
class Category(models.Model):
    id_category = models.BigAutoField(primary_key=True)
    name = models.CharField(verbose_name='Категория', max_length=50)
    subscribed = models.ManyToManyField(User, null=True, related_name='sub_category')

    def __str__(self):
        return f'{self.name}'


# модель Объявлений
class Posts(models.Model):
    id_Post = models.BigAutoField(primary_key=True)
    header = models.CharField(verbose_name="Заголовок", max_length=150)
    '''content = RichTextField()'''
    content = RichTextUploadingField('contents')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Пост_Пользователя')
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='Категория')

    def preview(self):
        size = 20 if len(self.content) > 20 else len(self.content)
        return self.content[:size] + '...'

    def get_absolute_url(self):
        return f'/posts/{self.id_Post}'

    def __str__(self):
        return f'{self.header}' \
               f'{self.content}' \
               f'{self.author}' \
               f'{self.category}'


class StatusFilterResponses(models.Manager):
    def get_queryset(self):

        return super().get_queryset().filter(Q(status=False, user=get_current_user()) |
                                             Q(status=False, post__author__username=get_current_user()) |
                                             Q(status=True))


# модель откликов
class Responses(models.Model):
    id_response = models.BigAutoField(primary_key=True)
    text = models.CharField(verbose_name='Отклик', max_length=500)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Отклик_Пользователя')
    post = models.ForeignKey('Posts', on_delete=models.CASCADE, related_name='responses_posts')
    status = models.BooleanField(verbose_name='Видимость статьи', default=False)
    objects = StatusFilterResponses()

    def __str__(self):
        return f'{self.text}' \
               f'{self.user}' \
               f'{self.post}' \
               f'{self.status}'
