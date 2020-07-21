import csv, io
from .models import Podcast, Category
from datetime import datetime
import threading


def upload_pods(request):
    # read csv file
    start_time = datetime.now()
    csv_file = request.FILES['file']
    data_set = csv_file.read().decode('UTF-8')
    io_string = io.StringIO(data_set)
    top_row = next(io_string)
    headings = top_row.split(",")
    counter = 0
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
            counter += 1
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
            counter += 1
    finish_time = datetime.now() - start_time
    print(f'{counter} rows added to DB in {finish_time}')