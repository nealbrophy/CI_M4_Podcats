from django.shortcuts import render, redirect, reverse, get_object_or_404
from .models import Review, Podcast
from .forms import ReviewForm
from django.contrib import messages
from .tasks import upload_reviews


def reviews(request):
    all_reviews = Review.objects.all()[:10]
    context = {
        "reviews": all_reviews,
    }
    return render(request, 'reviews/index.html', context)


def upload_review_data(request):
    """ A view to upload podcast data. """
    template = "reviews/upload_reviews.html"
    data = Review.objects.all()
    prompt = {
        'order': 'Order of the CSV should be uuid, title, friendly_title, image_url, language, categories, website',
        'reviews': data
    }

    if request.method == "GET":
        return render(request, template, prompt)

    for file in request.FILES:
        # check if file is CSV, if not present error
        if not request.FILES[file].name.endswith('.csv'):
            messages.error(request, 'THIS IS NOT A CSV FILE')
    upload_reviews(request)
    context = {}
    messages.success(request, f'Files added to upload queue.')
    return render(request, template, context)


def add_review(request, podcast_id):
    """
    A view for returning the add_review page
    and accepting using review submissions.
    """
    podcast = get_object_or_404(Podcast, pk=podcast_id)
    try:
        existing_review = Review.objects.filter(podcast_id=podcast_id, user_id=request.user.id)
    except Review.DoesNotExist:
        existing_review = None

    if existing_review:
        form = ReviewForm(instance=existing_review)

    else:
        form = ReviewForm({"podcast_id": podcast_id})

    template = "reviews/add_review.html"
    context = {
        "podcast": podcast,
        "form": form,
    }

    if request.method == "GET":
        return render(request, template, context)
    else:
        form = ReviewForm(request.POST, {"podcast_id": podcast_id})
        if form.is_valid():
            form.save()
            messages.success(request, "Review added!")
            return redirect(reverse('podcast_detail', args=[podcast.id]))
        else:
            messages.error(request, "Failed to add review. Please check the form is valid.")


def delete_all_reviews(request):
    """ A view to delete all reviews in the db. """

    template = "reviews/delete_all.html"
    # if GET return template
    if request.method == "GET":
        return render(request, 'reviews/delete_all.html')

    if "delete_reviews" in request.POST:
        # check if there are pods to delete in db
        if int(Review.objects.all().count()) > 0:
            Review.objects.all().delete()
            messages.success(request, 'Deleted successfully')
            return render(request, template)
        else:
            messages.error(request, 'Nothing to delete')
            return render(request, template)
