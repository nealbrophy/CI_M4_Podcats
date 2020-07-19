from .models import Podcast, Category
from datetime import datetime
import requests
import itunes


all_pods = Podcast.objects.all()


counter = 0

podcast = itunes.lookup(1313466221)
_, create = Podcast.objects.update_or_create(
    image_url=podcast.artwork['600'],
)


# for podcast in all_pods:
#     id = podcast.itunes_id
#     if not podcast.image_url or not podcast.website or not podcast.category or not podcast.description:
#         pod = itunes.lookup(id)
#         _, create = Podcast.objects.update_or_create(
#             image_url=pod.artwork['600'],
#             description=column[6],
#             website=pod.url,
#             category_id=pod.genre,
#         )
