import csv, io
from django.contrib.auth.models import User
from .models import Review
from pods.models import Podcast
from datetime import datetime
import random


def upload_reviews(request):
    for file in request.FILES:
        total_count = 0
        # read csv file
        all_users = User.objects.all()
        print(f"Starting to process {request.FILES[file].name}. Will let you know when done.")
        start_time = datetime.now()
        counter = 0
        data_set = request.FILES[file].read().decode('UTF-8')
        podcasts_in_db = Podcast.objects.all()
        io_string = io.StringIO(data_set)
        next(io_string)
        for column in csv.reader(io_string, delimiter=',', quotechar="|"):
            random_id = random.randint(1, 50000)
            random_user = all_users.filter(id=random_id).first()
            try:
                if podcasts_in_db.filter(uuid=column[0]).count() > 0:
                    _, create = Review.objects.update_or_create(
                        podcast_id=Podcast.objects.get(uuid=column[0].replace('"', '')),
                        title=column[1],
                        content=column[2],
                        rating=column[3],
                        created=column[4].replace('"', ''),
                        user=all_users.get(id=random_user.id),
                    )
                    counter += 1
                else:
                    next(io_string)
            except Exception as e:
                print(e)

        finish_time = datetime.now() - start_time
        total_count += counter
        print(f"{request.FILES[file].name} finished upload. Moving to next file...")
    print(f'Finished processing all files. {counter} rows added to DB in {finish_time}.')

