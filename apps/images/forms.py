from django import forms

from .models import Image


class ImageUploadForm(forms.ModelForm):
    image = forms.ImageField(
        widget=forms.ClearableFileInput(attrs={'multiple': True}))

    class Meta:
        model = Image
        fields = ['image', 'category', 'color', 'tags']


class ImageEditForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['category', 'color', 'tags']
