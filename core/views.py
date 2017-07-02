from django.shortcuts import redirect, render

from core.forms import DocumentForm


def model_form_upload(request):
    # if request is a POST, then process the form data
    # (i.e. user filled out the form and is sending data back)
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('homepage')
    # otherwise create the form
    # (i.e. user has not filled out the form)
    else:
        form = DocumentForm()
    return render(request, 'core/model_form_upload.html', {
        'form': form
    })
