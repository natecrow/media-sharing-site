from datetime import date

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

    def clean(self):
        cleaned_data = super(SignUpForm, self).clean()
        birth_date = cleaned_data.get('birth_date')

        if birth_date > date.today():
            raise forms.ValidationError("Birth date cannot be in the future.")

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name',
                  'email', 'password1', 'password2',)


class ProfilePictureUploadForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_picture']
