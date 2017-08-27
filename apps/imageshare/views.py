import logging

from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic.edit import FormView

from .forms import ImageUploadForm
from .models import Image

logger = logging.getLogger('uploads')


# @login_required(login_url='accounts:login')
class ImageUploadView(FormView):
    form_class = ImageUploadForm
    template_name = 'imageshare/upload_images.html'
    success_url = reverse_lazy('accounts:profile')

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
                logger.info('Saved mage \"' + f.name + '\"')
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
