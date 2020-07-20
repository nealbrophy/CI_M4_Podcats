import csv, io
from django.shortcuts import render
from .models import Review, Podcast
from django.contrib import messages
from datetime import datetime



def upload_review_data(request):
    """ A view to upload podcast data """
    template = "reviews/upload_reviews.html"
    data = Review.objects.all()
    prompt = {
        'order': 'Order of the CSV should be uuid, title, friendly_title, image_url, language, categories, website',
        'reviews': data
    }

    if request.method == "GET":
        return render(request, template, prompt)

    csv_file = request.FILES['file']

    if not csv_file.name.endswith('.csv'):
        messages.error(request, 'THIS IS NOT A CSV FILE')

    data_set = csv_file.read().decode('UTF-8')
    start_time = datetime.now()
    counter = 0
    podcasts_in_db = Podcast.objects.all()
    io_string = io.StringIO(data_set)
    next(io_string)
    for column in csv.reader(io_string, delimiter=',', quotechar="|"):
        if podcasts_in_db.filter(uuid=column[0]).count() > 0:
            _, create = Review.objects.update_or_create(
                podcast=Podcast.objects.get(uuid=column[0].replace('"', '')),
                title=column[1],
                content=column[2],
                rating=column[3],
                created=column[4].replace('"', ''),
            )
            counter += 1
        else:
            next(io_string)
    finish_time = datetime.now() - start_time
    messages.success(request, f'{counter} rows uploaded in {finish_time} from {csv_file.name}')
    context = {}
    return render(request, template, context)


def create_review(request):
    """
    A view for returning the add_review page
    and accepting using review submissions
    """

    if request.method == "GET":
        return render(request, )

def reviews(request):
    return render(request, 'reviews/index.html')
