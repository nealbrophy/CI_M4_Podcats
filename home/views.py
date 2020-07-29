import csv, io
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from .models import UserProfile
from .forms import ProfileForm
from reviews.models import Review
from pods.models import Podcast
from django.contrib.auth.models import User


def index(request):
    """ A view to return the index page. """

    return render(request, 'home/index.html')


@login_required
def dashboard(request):
    """ A view to return the dashboard page. """
    template = "home/dashboard.html"
    profile = get_object_or_404(UserProfile, user=request.user)
    podcasts = Podcast.objects.all()
    reviewed_pods = []
    try:
        reviews = Review.objects.filter(user=request.user)
    except Review.DoesNotExist:
        reviews = None

    if reviews:
        for review in reviews:
            reviewed_pods.append((review.id, Podcast.objects.get(id=review.podcast_id_id)))

    if request.method == "POST":
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated!")
        else:
            messages.error(request, "Update failed. Please recheck the form.")
    else:
        form = ProfileForm(instance=profile)
    context = {
        "profile": profile,
        "form": form,
        "reviews": reviews,
        "reviewed_pods": reviewed_pods,
    }

    return render(request, template, context)


@login_required
def upload_users(request):
    """ A view to upload users to the db. """

    if request.method == "GET":
        return render(request, "home/upload_users.html")
    # otherwise capture file upload
    csv_file = request.FILES["file"]
    # validate is csv
    if not csv_file.name.endswith(".csv"):
        messages.error(request, "THIS IS NOT A CSV FILE")
    # read file
    data_set = csv_file.read().decode("UTF-8")
    io_string = io.StringIO(data_set)
    next(io_string)
    # upload to db
    for column in csv.reader(io_string, delimiter=",", quotechar="|"):
        _, create = User.objects.update_or_create(
            username=column[0].lower(),
            email=column[1],
        )
    context = {}
    return render(request, "home/upload_users.html", context)
