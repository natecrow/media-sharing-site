from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Profile


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    email = forms.EmailField(max_length=254, help_text='Required.')
    birth_date = forms.DateField(widget=forms.widgets.DateInput(
        attrs={'type': 'date'}), required=False)
    gender = forms.ChoiceField(
        choices=[(s.value, s.name) for s in Profile.Genders], required=False)
    location = forms.CharField(max_length=30, required=False)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name',
                  'email', 'password1', 'password2',)


class ProfilePictureUploadForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_picture']
