from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    country = models.CharField(max_length=30, blank=True)
    city = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    email_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return self.country + self.city


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()


class Post(models.Model):
    title = models.CharField(max_length=30)
    description = models.TextField(max_length=500)
    body = models.TextField(max_length=1000)
    image = models.TextField(max_length=200)
