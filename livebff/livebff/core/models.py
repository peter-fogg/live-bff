from django.contrib.auth.models import User
from django.contrib.gis.db.models import PointField
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    """
    Profile for a user. Gives a short biography and birthdate.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100, default='')
    bio = models.TextField(max_length=500, blank=True)
    birth_date = models.DateField(null=True)
    location = PointField(null=True, blank=True)

    def is_active(self):
        """
        Returns True if the user has filled out their profile and can be shown in the list of users.
        """
        return self.bio != '' and self.full_name != ''

@receiver(post_save, sender=User)
def update_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
