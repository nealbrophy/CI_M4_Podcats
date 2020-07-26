from django.contrib import messages
from django.shortcuts import render, reverse, redirect
from django.conf import settings
import requests
from pods.models import Podcast, Category
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import itunes


def basic_search(request):
    """ A view to return results from the navbar search """
    all_pods = Podcast.objects.all()
    query = None
    if request.method == "GET":
        if "q" in request.GET:
            query = request.GET["q"]
            if not query:
                messages.error(request, "You didn't enter any search criteria!")
                return redirect(reverse('index'))
    queries = Q(title__icontains=query) | Q(description__icontains=query) | Q(uuid__icontains=query)
    if not all_pods.filter(queries):
        itunes_results = []
        raw_response = requests.get(f'{settings.ITUNES_SEARCH_URL}term={query}&entity=podcast,podcastAuthor')
        response = raw_response.json()

        for i in range(response["resultCount"]):
            itunes_results.append({
                    "itunes_id": response["results"][i]["collectionId"],
                    "title": response["results"][i]["collectionName"].replace(" ", "_"),
                    "friendly_title": response["results"][i]["collectionName"],
                    "image_url": response["results"][i]["artworkUrl600"],
                    "category": response["results"][i]["genres"],
            })
        return render(request, 'search/results.html', {
            "itunes_results": itunes_results,
        })
    else:
        podcasts = all_pods.filter(queries)
        print(podcasts)

        page = request.GET.get('page', 1)
        paginator = Paginator(podcasts, 20)

        try:
            results = paginator.page(page)
        except PageNotAnInteger:
            results = paginator.page(1)
        except EmptyPage:
            results = paginator.page(paginator.num_pages)

        index = results.number - 1
        max_index = len(paginator.page_range)
        start_index = index - 3 if index >= 3 else 0
        end_index = index + 3 if index <= max_index - 3 else max_index
        page_range = list(paginator.page_range)[start_index:end_index]

        return render(request, 'search/results.html', {
            "results": results,
            "page_range": page_range
        })

    # else:
    #     podcast = request.POST['q'].replace(' ', '%20')
    #
    #     url = f'https://listen-api.listennotes.com/api/v2/search?q={podcast}&sort_by_date=0&type=podcast&only_in=title%2Cdescription&safe_mode=0'
    #     headers = {
    #         'X-ListenAPI-Key': settings.LISTEN_KEY,
    #     }
    #     response = requests.request('GET', url, headers=headers)
    #     results = response.json()["results"]
    #     podcasts = []
    #     for podcast in results:
    #         podcasts.append({
    #             "image_url": podcast['image'],
    #             "title": podcast["title_original"],
    #             "description": podcast["description_original"]
    #         })
    #     context = {
    #         'podcasts': podcasts,
    #     }
    #     return render(request, 'search/results.html', context)
