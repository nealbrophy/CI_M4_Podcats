import csv, io
from .models import Podcast, Category
from datetime import datetime
from concurrent.futures.thread import ThreadPoolExecutor


# def queue_manager(request):
#     with ThreadPoolExecutor(max_workers=1) as executor:
#         job = executor.submit(upload_pods, request)
#     return job.result()


def upload_pods(request):
    output_message = []
    total_count = 0
    # read csv file
    for file in request.FILES:
        print(f"Starting to process {request.FILES[file].name}. Will let you know when done.")
        start_time = datetime.now()
        data_set = request.FILES[file].read().decode('UTF-8')
        io_string = io.StringIO(data_set)
        top_row = next(io_string)
        headings = top_row.split(",")
        print(headings)
        if "category" in headings:
            print(top_row)
        counter = 0
        # skip headings
        next(io_string)
        for column in csv.reader(io_string, delimiter=',', quotechar="|"):
            # if csv contains category column upload data with category
            if "category" in headings:
                _, create = Podcast.objects.update_or_create(
                    uuid=column[0],
                    itunes_id=column[1],
                    title=column[2].lower(),
                    friendly_title=column[3],
                    itunes_url=column[4],
                    image_url=column[5],
                    description=column[6],
                    category_id=column[7],
                    website=column[8],

                )
                counter += 1
            # if csv doesn't contain category column upload data without category
            else:
                _, create = Podcast.objects.update_or_create(
                    uuid=column[0],
                    itunes_id=column[1],
                    title=column[2].lower(),
                    friendly_title=column[3],
                    itunes_url=column[4],
                    image_url=column[5],
                    description=column[6],
                    website=column[7],
                )
                counter += 1
        finish_time = datetime.now() - start_time
        total_count += counter
        print(f'{counter} rows added to DB in {finish_time} from {request.FILES[file].name}')
    return total_count
