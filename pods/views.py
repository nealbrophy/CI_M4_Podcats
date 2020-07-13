import csv, io
from django.shortcuts import render
from .models import Podcast, Category
from django.contrib import messages

def pods(request):
    """ A view to return the Pods page """
    form = Podcast
    context = {
        'form': form,
    }
    return render(request, 'pods/pods.html', context)

def upload_pod_data(request):
    """ A view to upload podcast data """
    template = "pods/upload_pods.html"
    data = Podcast.objects.all()
    prompt = {
        'order': 'Order of the CSV should be uuid, title, friendly_title, image_url, language, categories, website',
        'podcasts': data
    }

    if request.method == "GET":
        return render(request, template, prompt)

    csv_file = request.FILES['file']

    if not csv_file.name.endswith('.csv'):
        messages.error(request, 'THIS IS NOT A CSV FILE')

    data_set = csv_file.read().decode('UTF-8')

    io_string = io.StringIO(data_set)
    next(io_string)
    for column in csv.reader(io_string, delimiter=',', quotechar="|"):
        _, create = Podcast.objects.update_or_create(
            uuid=column[0],
            title=column[1],
            friendly_title=column[2],
            image_url=column[3],
            language=column[4],
            category=column[5],
            website=column[6],
        )
    context = {}
    return render(request, template, context)

def upload_category_data(request):
    """ A view to upload podcast category data """
    template = "pods/upload_cats.html"
    data = Category.objects.all()
    prompt = {
        'order': 'Order of the CSV should be pk, name, friendly_name',
        'categories': data
    }

    if request.method == "GET":
        return render(request, template, prompt)

    csv_file = request.FILES['file']

    if not csv_file.name.endswith('.csv'):
        messages.error(request, 'THIS IS NOT A CSV FILE')

    data_set = csv_file.read().decode('UTF-8')

    io_string = io.StringIO(data_set)
    next(io_string)
    for column in csv.reader(io_string, delimiter=',', quotechar="|"):
        _, create = Category.objects.update_or_create(
            pk=column[0],
            name=column[1],
            friendly_name=column[2],
        )
    context = {}
    return render(request, template, context)

def delete_all(request):
    """ A view to delete all pods """
    template = "pods/delete_all.html"
    if request.method == "GET":
        return render(request, 'pods/delete_all.html')
    else:
        if int(Podcast.objects.all().count()) > 0:
            Podcast.objects.all().delete()
            messages.success(request, 'Deleted successfully')
            return render(request, template)
        else:
            messages.error(request, 'Nothing to delete')
            return render(request, template)