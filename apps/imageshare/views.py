import logging

from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import FormView

from .forms import ImageUploadForm
from .models import Image

logger = logging.getLogger('uploads')


# @login_required(login_url='accounts:login')
class ImageUploadView(FormView):
    form_class = ImageUploadForm
    template_name = 'imageshare/upload_images.html'
    success_url = reverse_lazy('accounts:edit_profile')

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        files = request.FILES.getlist('image')
        if form.is_valid():
            for f in files:
                logger.info(
                    'Creating model for image: \"' + f.name + '\"')
                image = Image(image=f, user=request.user)
                image.save()
                logger.info('Saved image \"' + f.name + '\"')
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


def images(request):
    picture_list = Image.objects.all().order_by('uploaded_date')

    paginator = Paginator(picture_list, 20)  # Number of pictures per page

    page = request.GET.get('page')
    try:
        pictures = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        pictures = paginator.page(1)
    except EmptyPage:
        # If page is out of range, deliver last page of results.
        pictures = paginator.page(paginator.num_pages)

    # get list of tags from all images
    tags = []
    for picture in picture_list:
        for tag in picture.tags.all():
            if tag not in tags:
                tags.append(tag)
    # sort tags alphabetically
    tags.sort(key=lambda x: x.name)

    context = {'pictures': pictures, 'tags': tags}

    return render(request, 'imageshare/images.html', context)
