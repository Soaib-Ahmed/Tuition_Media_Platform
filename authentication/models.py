from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from django.db import models


# Create your models here.
class ChangeUserData(UserChangeForm):
    password = None
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email']


GENDER_TYPE = (
    ('Male', 'Male'),
    ('Female', 'Female'),
)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=1000, verbose_name='Bio')
    location = models.CharField(max_length=1000, verbose_name='Location')
    gender = models.CharField(max_length=10, choices=GENDER_TYPE)
    expertise = models.CharField(max_length=1000, verbose_name='Expertise')
    profile_img = models.ImageField(upload_to='authentication/media/uploads/', blank=True, null=True)
    email_confirmed = models.BooleanField(default=False, verbose_name='Email Confirmed')