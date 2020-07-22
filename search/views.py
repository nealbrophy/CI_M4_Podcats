from django.shortcuts import render
from django.conf import settings
import requests
from pods.models import Podcast, Category
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def basic_search(request):
    """ A view to return results from the navbar search """

    if True:
        query = request.POST['q']
        all_pods = Podcast.objects.all()
        queries = Q(title__icontains=query) | Q(description__icontains=query) | Q(uuid__icontains=query)
        podcasts = all_pods.filter(queries)
        page = request.GET.get('page', 1)
        paginator = Paginator(podcasts, 20)
        try:
            results = paginator.page(page)
        except PageNotAnInteger:
            results = paginator.page(1)
        except EmptyPage:
            results = paginator.page(paginator.num_pages)

        return render(request, 'search/results.html', {'results': results})

    else:
        podcast = request.POST['q'].replace(' ', '%20')

        url = f'https://listen-api.listennotes.com/api/v2/search?q={podcast}&sort_by_date=0&type=podcast&only_in=title%2Cdescription&safe_mode=0'
        headers = {
            'X-ListenAPI-Key': settings.LISTEN_KEY,
        }
        response = requests.request('GET', url, headers=headers)
        results = response.json()["results"]
        podcasts = []
        for podcast in results:
            podcasts.append({
                "image_url": podcast['image'],
                "title": podcast["title_original"],
                "description": podcast["description_original"]
            })
        context = {
            'podcasts': podcasts,
        }
        return render(request, 'search/results.html', context)
