from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User,
                                on_delete=models.CASCADE,
                                null=True)
    wins = models.PositiveIntegerField(default=0)

class Tourney(models.Model):
    player = models.ManyToManyField(Profile)
    name = models.CharField(max_length=30,
                            null=True,
                            blank=False,)
    winner = models.ForeignKey(Profile,
                               on_delete=models.CASCADE,
                               null=True,
                               blank=True,
                               related_name='tourneywinner')

class Match(models.Model):
    winner = models.ForeignKey(Profile,
                               on_delete=models.CASCADE,
                               null=True,
                               blank=True,
                               related_name='matchwinner',)
    player1 = models.ForeignKey(Profile,
                                on_delete=models.CASCADE,
                                null=True,
                                blank=False,
                                related_name='player1',)
    player2 = models.ForeignKey(Profile,
                                on_delete=models.CASCADE,
                                null=True,
                                blank=False,
                                related_name='player2',)
    tourney = models.ForeignKey(Tourney,
                                on_delete=models.CASCADE,
                                null=True,
                                blank=False,
                                related_name='tourney')

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

