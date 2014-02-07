from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

# Create your models here.

class UserProfile(models.Model):
    # This field is required.
    user = models.OneToOneField(User)

    # Other fields here
    fullname = models.CharField(max_length=40)
    address = models.CharField(max_length=40)
    region = models.CharField(max_length=40)
    interests = models.CharField(max_length=60)

    def __unicode__(self):
        return "%s's profile" % self.user.username
    

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)

#SeedType Model
class SeedType(models.Model):

    name = models.CharField(max_length=100)
    sci_name = models.CharField(max_length=100)

    season_start = models.CharField(max_length=100)
    season_end = models.CharField(max_length=100)
    region = models.CharField(max_length=100)
    
    spec_req = models.TextField()
    tips = models.TextField()
    harvest_info = models.TextField()
    description = models.TextField()

    verified = models.BooleanField()
    gmo_flag = models.NullBooleanField()

    #pic = models.ImageField()

    def __unicode__(self):
        return self.name

#Inventory Model
class Inventory(models.Model):

    user_profile= models.OneToOneField(UserProfile)

    def __unicode__(self):
        return "%s's inventory" % self.user_profile.user.username

def create_inventory(sender, instance, created, **kwargs):
    if created:
        Inventory.objects.create(user_profile=instance)

post_save.connect(create_inventory, sender=UserProfile)

#Item Model
class Item(models.Model):

    amount = models.IntegerField()
    kind = models.ForeignKey(SeedType)
    inventory = models.ForeignKey(Inventory)

    def __unicode__(self):
        return "%d %s" % (self.amount,self.kind.__unicode__())
