from django.db import models
from django.contrib.auth.models import User

class Topic(models.Model):
    """Данные о теме"""
    text = models.CharField(max_length = 200)
    date_added = models.DateTimeField(auto_now_add = True)
    owner = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        """Возвращает название темы"""
        return self.text

class Entry(models.Model):
    """Записи в темах"""
    topic = models.ForeignKey(Topic, on_delete = models.CASCADE)
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add = True)

    class Meta:
        verbose_name_plural = "enteries"

    def __str__(self):
        """Возвращается информация для обращения к отдельным записям"""
        return f"{self.text[:50]}..."