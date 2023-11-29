import uuid

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class IntegerRangeField(models.IntegerField):
    def __init__(self, verbose_name=None, name=None, specie=None, min_value=None, *kwargs):
        self.min_value = min_value
        models.IntegerField.__init__(self, verbose_name, name, specie, *kwargs)

    def formfield(self, *kwargs):
        defaults = {'min_value': self.min_value}
        defaults.update(*kwargs)
        return super(IntegerRangeField, self).formfield(**defaults)


class Silmarillion(models.Model):
    name = models.CharField(max_length=200, primary_key= True, verbose_name="Обитатели Сильмариллиона",
                            help_text="Введите эпоху (Календарь Нуменора)", null=False, blank=False)
    description = models.TextField(verbose_name="эпоха")


    def __str__(self):
        return "Эпоха " + self.name

    class Meta:
        db_table = "sillis"


class Status(models.Model):
    status = models.CharField(max_length=200, verbose_name="Класс",
                              help_text="Введите класс", default="")
    def __str__(self):
        return "Класс " + self.status

    class Meta:
        db_table = "Status"

class Being(models.Model):
    specie = models.CharField(max_length=100, verbose_name="Вид",
                              help_text="Введите расу", null=False, blank=False)
    name = models.CharField(max_length=200, verbose_name="Имя",
                            help_text="Введите Имя", null=False, blank=False)
    age = models.IntegerField(max_length=200, verbose_name="Возраст",
                            help_text="Введите возраст", null=False, blank=False )
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    time = models.ForeignKey(Silmarillion, on_delete=models.CASCADE)
    id_being = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Магия",
                              help_text="Введите уровень владения магии", null=True, blank=True)

    def __str__(self):
        return "Принадлежность: " + self.specie + " " + self.name + " " + self.age.__str__() + " " + self.time.__str__()

    class Meta:
        db_table = "Creature"
# Create your models here.

class Person(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    position = models.CharField(max_length=200, verbose_name="Ранг в гильдии", default="Игрок")
    specie = models.CharField(max_length=200, default="", blank=True)
    status = models.ForeignKey(Status, on_delete=models.CASCADE)


    def __str__(self):
        return "Личная информация: " + " " + self.user.username + " " + self.specie + " " + self.position+" " + self.status
    class Meta:
        db_table = "Person"
