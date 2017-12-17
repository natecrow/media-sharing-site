from django.contrib import admin

from .models import Image


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    fields = ['image', 'user', 'uploaded_date', 'category', 'color', 'tags']
    readonly_fields = ['uploaded_date']
    list_display = ['__str__', 'user', 'uploaded_date']
    list_display_links = ['__str__']
