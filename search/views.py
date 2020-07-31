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
                return redirect(reverse("home"))
    queries = Q(title__icontains=query) | Q(description__icontains=query) | Q(uuid__icontains=query)
    if not all_pods.filter(queries):
        q = request.GET["q"]
        return search_itunes(request, q)
    else:
        podcasts = all_pods.filter(queries)

        page = request.GET.get("page", 1)
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


def search_itunes(request, q):
    """ A view to return results via the iTunes API """
    query = q
    itunes_results = []
    raw_response = requests.get(f"{settings.ITUNES_SEARCH_URL}term={query}&entity=podcast")
    response = raw_response.json()
    print(response)
    for i in range(response["resultCount"]):
        itunes_results.append({
            "itunes_id": response["results"][i]["collectionId"],
            "title": response["results"][i]["collectionName"].replace(" ", "_"),
            "friendly_title": response["results"][i]["collectionName"],
            "image_url": response["results"][i]["artworkUrl600"],
            "category": response["results"][i]["genres"],
        })
    context = {
        "q": query,
        "itunes_results": itunes_results,
    }
    return render(request, 'search/results.html', context)
