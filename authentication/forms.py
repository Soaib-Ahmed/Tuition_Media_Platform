from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from .models import UserProfile

GENDER_TYPE = (
    ('Male', 'Male'),
    ('Female', 'Female'),
)

# class SignupForm(UserCreationForm):
#   first_name = forms.CharField(widget=forms.TextInput(attrs={'id' : 'required'}))
#   last_name = forms.CharField(widget=forms.TextInput(attrs={'id' : 'required'}))
#   email = forms.CharField(widget=forms.EmailInput(attrs={'id' : 'required'}))
#   class Meta:
#       model = User
#       fields = ['username', 'first_name', 'last_name', 'email']

    
# class ChangeUserData(UserChangeForm):
#     password = None
#     class Meta:
#         model = User
#         fields = ['username','first_name','last_name','email']

class SignupForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'id': 'required'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'id': 'required'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'id': 'required'}))
    bio = forms.CharField(max_length=1000, required=False, label='Bio')
    location = forms.CharField(max_length=1000, required=False, label='Location')
    gender = forms.ChoiceField(choices=GENDER_TYPE, required=False, label='Gender')
    expertise = forms.CharField(max_length=1000, required=False, label='Expertise')
    profile_img = forms.ImageField(required=False, label='Profile Image')

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'bio', 'location', 'gender', 'expertise', 'profile_img']

class ChangeUserData(UserChangeForm):
    password = None
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio', 'location', 'gender', 'expertise', 'profile_img']