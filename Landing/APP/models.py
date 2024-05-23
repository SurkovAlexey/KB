from django.db import models

# Create your models here.

class Client(models.Model):
    name = models.CharField(max_length=100, verbose_name='Ваше имя')
    phone = models.CharField(max_length=100, verbose_name='Ваш email')
    question = models.TextField(verbose_name='Ваш вопрос')
    
    def __str__(self):
        return self.name
