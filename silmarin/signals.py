from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Person, Being

@receiver(post_save, sender=User)
def create_person(sender, instance, created, **kwargs):
    if created:
        specie = Being.objects.filter(name=instance.first_name).values_list('specie', flat=True).first()
        Person.objects.create(user=instance, specie=specie, position="Игрок")