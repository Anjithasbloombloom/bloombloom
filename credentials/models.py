# models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from allauth.account.adapter import DefaultAccountAdapter
from django.contrib.auth import get_user_model

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True) 
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)

    # Override fields to remove them from the built-in user model
    last_login = None
    # is_superuser = None
    first_name = None
    last_name = None
    # is_staff = None
    # is_active = None
    date_joined = None


    
    class Meta:
        permissions = [
            ("can_do_something", "Can do something"),
            # Add other permissions as needed
        ]
        


    groups = models.ManyToManyField('auth.Group', related_name='custom_user_set', blank=True, verbose_name='groups')
    user_permissions = models.ManyToManyField('auth.Permission', related_name='custom_user_set', blank=True, verbose_name='user permissions')



class Purpose(models.Model):
    purpose_name = models.CharField(max_length=100)

# Model to store interest
class Interest(models.Model):
    interest_name = models.CharField(max_length=100)

# Model to store User details which contain the interest and purpose selected by the user
class User_detail(models.Model):
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    purposes = models.ManyToManyField(Purpose)
    interests = models.ManyToManyField(Interest)




# added **kwargs to accept unexpected values

class CustomAccountAdapter(DefaultAccountAdapter):
    def get_user_model(self):
        return CustomUser

    def clean_username(self, username,**kwargs):
        return username




