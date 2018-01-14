import logging
import os

from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import render
from django.urls import reverse
from django.views.generic.edit import FormView

from .forms import ImageUploadForm, ImageEditForm
from .models import Image

logger = logging.getLogger('uploads')


# @login_required(login_url='accounts:login')
class ImageUploadView(FormView):
    form_class = ImageUploadForm
    template_name = 'images/upload_images.html'

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        files = request.FILES.getlist('image')
        if form.is_valid():
            for f in files:
                logger.info(
                    'Creating model for image: \"' + f.name + '\"')
                image = Image(image=f, user=request.user)
                image.tags = form.cleaned_data['tags']
                image.save()
                logger.info('Saved image \"' + f.name + '\"')
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_success_url(self):
        username = self.request.user.username
        return reverse('accounts:profile_page', kwargs={'username': username})


def images(request):
    # filter images by any given tags, otherwise show all images
    selected_tags = request.GET.getlist('tag')
    if selected_tags:
        # handle spaces in any tags
        selected_tags = [tag.replace('-', ' ') for tag in selected_tags]
        image_list = Image.objects.filter(
            tags=','.join(selected_tags)).order_by('uploaded_date')
    else:
        image_list = Image.objects.all().order_by('uploaded_date')

    # get list of tags from all images
    tags = []
    for image in Image.objects.all():
        for tag in image.tags.all():
            if tag not in tags and tag not in selected_tags:
                tags.append(tag)
    # sort tags alphabetically
    tags.sort(key=lambda x: x.name)

    paginator = Paginator(image_list, 20)  # Number of pictures per page
    page = request.GET.get('page')
    try:
        image = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        image = paginator.page(1)
    except EmptyPage:
        # If page is out of range, deliver last page of results.
        image = paginator.page(paginator.num_pages)

    url_query_string = request.GET.urlencode()

    context = {'pictures': image, 'page': page,
               'tags': tags, 'selected_tags': selected_tags,
               'url_query_string': url_query_string}

    return render(request, 'images/images.html', context)


def view_image(request, image_id):
    picture = Image.objects.get(id=image_id)
    form = ImageEditForm(request.POST or None, instance=picture)

    if request.method == "POST" and form.is_valid():
        form.save()

    picture_basename = os.path.basename(picture.image.name)
    picture_upload_date = picture.uploaded_date.date()

    context = {'picture': picture, 'form': form, 'picture_basename': picture_basename,
               'picture_upload_date': picture_upload_date}

    return render(request, 'images/view_image.html', context)
