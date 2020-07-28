import csv, io
from django.conf import settings
from django.db.models import Count
from django.shortcuts import render, redirect, reverse, get_object_or_404
from .forms import PodcastForm
from .models import Podcast, Category
from reviews.models import Review
from reviews.forms import ReviewForm
from django.contrib import messages
from django.contrib.auth.models import User
from .tasks import upload_pods
import requests
from django.contrib.auth.decorators import login_required


def top_podcasts(request):
    """ A view to return the Pods page """
    pods = Podcast.objects.annotate(num_reviews=Count('review')).order_by('-num_reviews')[:10]
    # podcasts = Podcast.objects.all()
    # for podcast in podcasts:
    #     try:
    #         reviews = Review.objects.filter(podcast_id=podcast.id).count()
    #     except Review.DoesNotExist:
    #         reviews = 0
    #     review_count.append((reviews, podcast.id))

    top_ten = []
    for pod in pods:
        top_ten.append((pod.image_url, pod.friendly_title, pod.num_reviews))


    context = {
        "pods": pods,
        "top_ten": top_ten,
    }

    return render(request, 'pods/top_podcasts.html', context)


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
    file_count = 0
    for file in request.FILES:
        # check if file is CSV, if not present error
        file_count += 1
        if not request.FILES[file].name.endswith('.csv'):
            messages.error(request, 'THIS IS NOT A CSV FILE')
    upload_pods(request)
    context = {}
    # messages.success(request, f'Upload complete! {upload} rows added to DB from {file_count} files.')
    messages.success(request, f'Files added to upload queue.')
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
            name=column[1].lower(),
            friendly_name=column[2],
        )
    context = {}
    return render(request, template, context)


@login_required
def delete_all(request):
    """ A view to delete all pods from db """
    template = "pods/delete_all.html"
    if request.user.is_superuser:
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
            elif 'fix_description' in request.POST:
                for pod in Podcast.objects.all():
                    try:
                        if pod.description.count() < 10:
                            pod(description=f"The {pod.friendly_title} podcast.")
                            pod.save()
                        messages.success(request, 'descriptions fixed')
                        return render(request, template)
                    except Exception as e:
                        messages.error(request, f'Unable to complete due to {e}')
    else:
        messages.error(request, "Sorry, you don't have permission to do that.")
        return render(request, 'pods/pods.html')


@login_required
def add_podcast(request):
    """
    A view to return the PodcastForm
    and allow user to add a single podcast to db
    """

    user = User.objects.get(pk=request.user.id).userprofile

    if user.pro_user:
        podcast_form = PodcastForm()
        template = 'pods/add_podcast.html'
        context = {
            "form": podcast_form,
        }
        if request.method == "POST":
            form = PodcastForm(request.POST, request.FILES)
            if form.is_valid():
                form.clean_title()
                form.save()
                messages.success(request, "Successfully added podcast!")
                return redirect(reverse("add_podcast"))
            else:
                messages.error(request, "Failed to add podcast. Please ensure the form is valid.")
        else:
            return render(request, template, context)
    else:
        messages.error(request, "Sorry, you need to have a Pro account to do that.")
        return render(request, 'pods/pods.html')


def podcast_detail(request, id):
    """ A vew to show a specific podcast page. """
    if request.user:
        try:
            profile = User.objects.get(pk=request.user.id).userprofile
        except User.DoesNotExist:
            profile = None
    #     try:
    #         this_user_review = Review.objects.filter(user_id=request.user.id, podcast_id=id)
    #     except Review.DoesNotExist:
    #         this_user_review = None
    #
    # if this_user_review:
    #     review_form = ReviewForm(instance=this_user_review.id)
    # else:
    #     review_form = ReviewForm()

    from_page = request.META.get("HTTP_REFERER", "/")
    podcast = get_object_or_404(Podcast, pk=id)
    form = PodcastForm(instance=podcast)
    all_reviews = Review.objects.all()
    if all_reviews.filter(podcast_id=id).count() > 0:
        total_rating = 0
        review_count = 0
        reviews = all_reviews.filter(podcast_id=id)
        for review in reviews:
            review_count += 1
            total_rating += int(review.rating)
        average_rating = total_rating / review_count

    else:
        reviews = None
        average_rating = None
        review_count = 0

    context = {
        "podcast": podcast,
        "reviews": reviews,
        "from_page": from_page,
        "form": form,
        "average": average_rating,
        "review_count": review_count,
        "profile": profile,
        # "this_user_review": this_user_review,
        # "review_form": review_form,
    }

    return render(request, "pods/podcast_detail.html", context)


@login_required()
def import_from_itunes(request, id):
    user = User.objects.get(pk=request.user.id).userprofile

    if user.pro_user:
        itunes_lookup = requests.get(f'{settings.ITUNES_LOOKUP_URL}{id}')
        result = itunes_lookup.json()
        # this_id = result["results"][0]["collectionId"]
        # this_title = result["results"]["collectionName"].replace(" ", "_").lower()

        Podcast.objects.update_or_create(
            itunes_id=result["results"][0]["collectionId"],
            title=result["results"][0]["collectionName"].replace(" ", "_").lower(),
            friendly_title=result["results"][0]["collectionName"],
            image_url=result["results"][0]["artworkUrl600"],
            itunes_url=result["results"][0]["collectionViewUrl"],
        )

        try:
            category_lookup = Category.objects.get(friendly_name=result["results"][0]["primaryGenreName"]).id
            messages.info(request, "Please populate the description field as iTunes API doesn't supply that.")
        except Category.DoesNotExist:
            category_lookup = 0
            messages.info(request, "Please populate the description field and categories.")

        this_uuid = Podcast.objects.get(itunes_id=id).uuid
        pod = Podcast.objects.get(uuid=this_uuid)

        pod.category.set(str(category_lookup))

        context = {
            "id": this_uuid
        }
        return redirect(reverse("edit_podcast", args=[pod.id]))
    else:
        messages.error(request, "Sorry, you need to have a Pro account to do that.")
        return render(request, 'pods/pods.html')


@login_required
def edit_podcast(request, id):
    """ A view to edit a specific podcast """
    user = User.objects.get(pk=request.user.id).userprofile

    if user.pro_user:
        podcast = get_object_or_404(Podcast, pk=id)
        if request.method == "POST":
            form = PodcastForm(request.POST, request.FILES, instance=podcast)
            if form.is_valid():
                form.save()
                messages.success(request, "Podcast updated!")
                return redirect(reverse('podcast_detail', args=[podcast.id]))
            else:
                messages.error(request, "Failed to update. Please check the form is valid.")
        else:
            form = PodcastForm(instance=podcast)
            messages.info(request, f"You are editing {podcast.friendly_title}")
        template = "pods/edit_podcast.html"
        context = {
            "form": form,
            "podcast": podcast,
        }

        return render(request, template, context)
    else:
        messages.error(request, "Sorry, you need to have a Pro account to do that.")
        return render(request, 'pods/pods.html')


@login_required
def delete_podcast(request, id):
    """ A view to delete a specific podcast"""
    user = User.objects.get(pk=request.user.id).userprofile
    podcast = get_object_or_404(Podcast, pk=id)
    if user.pro_user:
        if request.method == "GET":
            form = PodcastForm(instance=podcast)
            template = "pods/delete_podcast.html"
            context = {
                "form": form,
                "podcast": podcast,
            }
            return render(request, template, context)
        else:
            podcast.delete()
            messages.success(request, "Podcast successfully deleted.")
            return redirect(reverse("home"))
    else:
        messages.error(request, "Sorry, you need to have a Pro account to do that.")
        return render(request, 'pods/pods.html')
