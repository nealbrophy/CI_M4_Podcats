import csv, io
from django.shortcuts import render
from .forms import PodcastForm
from .models import Podcast, Category
from django.contrib import messages


def pods(request):
    """ A view to return the Pods page """

    return render(request, 'pods/pods.html')


def upload_pod_data(request):
    """ A view to bulk upload podcast data via csv """
    template = "pods/upload_pods.html"
    data = Podcast.objects.all()
    prompt = {
        'order': 'Order of the CSV should be uuid, title, friendly_title, image_url, language, categories, website',
        'podcasts': data
    }
    # if GET return template
    if request.method == "GET":
        return render(request, template, prompt)
    # otherwise, capture uploaded file
    csv_file = request.FILES['file']
    # check if file is CSV, if not present error
    if not csv_file.name.endswith('.csv'):
        messages.error(request, 'THIS IS NOT A CSV FILE')
    # read csv file
    data_set = csv_file.read().decode('UTF-8')
    io_string = io.StringIO(data_set)
    top_row = next(io_string)
    headings = top_row.split(",")
    # skip headings
    next(io_string)
    for column in csv.reader(io_string, delimiter=',', quotechar="|"):
        # if csv contains category column upload data with category
        if "category" in headings:
            _, create = Podcast.objects.update_or_create(
                uuid=column[0],
                itunes_id=column[1],
                title=column[2],
                friendly_title=column[3],
                itunes_url=column[4],
                image_url=column[5],
                description=column[6],
                website=column[7],
                category_id=column[8],
            )
        # if csv doesn't contain category column upload data without category
        else:
            _, create = Podcast.objects.update_or_create(
                uuid=column[0],
                itunes_id=column[1],
                title=column[2],
                friendly_title=column[3],
                itunes_url=column[4],
                image_url=column[5],
                description=column[6],
                website=column[7],
            )
    messages.success(request, 'UPLOAD SUCCESSFUL')
    context = {}
    return render(request, template, context)


def upload_category_data(request):
    """ A view to bulk upload podcast category data via csv """
    template = "pods/upload_cats.html"
    data = Category.objects.all()
    prompt = {
        'order': 'Order of the CSV should be pk, name, friendly_name',
        'categories': data
    }
    # if GET return template
    if request.method == "GET":
        return render(request, template, prompt)
    # otherwise capture file upload
    csv_file = request.FILES['file']
    # validate is csv
    if not csv_file.name.endswith('.csv'):
        messages.error(request, 'THIS IS NOT A CSV FILE')
    # read file
    data_set = csv_file.read().decode('UTF-8')
    io_string = io.StringIO(data_set)
    next(io_string)
    # upload to db
    for column in csv.reader(io_string, delimiter=',', quotechar="|"):
        _, create = Category.objects.update_or_create(
            pk=column[0],
            name=column[1],
            friendly_name=column[2],
        )
    context = {}
    return render(request, template, context)


def delete_all(request):
    """ A view to delete all pods from db """
    template = "pods/delete_all.html"
    # if GET return template
    if request.method == "GET":
        return render(request, 'pods/delete_all.html')
    else:
        if "duplicates" in request.POST:
            for pod in Podcast.objects.all().reverse():
                if Podcast.objects.filter(uuid=pod.uuid).count() > 1:
                    pod.delete()
        elif "pods" in request.POST:
            # check if there are pods to delete in db
            if int(Podcast.objects.all().count()) > 0:
                Podcast.objects.all().delete()
                messages.success(request, 'Deleted successfully')
                return render(request, template)
            else:
                messages.error(request, 'Nothing to delete')
                return render(request, template)

def add_podcast(request):
    """
    A view to return the PodcastForm
    and allow user to add a single podcast to db
    """

    form = PodcastForm()
    template = 'pods/add_podcast.html'
    context = {
        "form": form,
    }
    if request.method == "GET":
        return render(request, template, context)