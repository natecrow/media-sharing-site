from django import forms

from .models import Image


class ImageUploadForm(forms.ModelForm):
    image = forms.ImageField(
        widget=forms.ClearableFileInput(attrs={'multiple': True}))

    class Meta:
        model = Image
        fields = ['image', 'tags']


class TagForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['tags']