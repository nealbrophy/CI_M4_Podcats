from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from .models import UserProfile
from .forms import ProfileForm
from django.contrib.auth.models import User

def index(request):
    """ A view to return the index page. """

    return render(request, 'home/index.html')


@login_required
def dashboard(request):
    """ A view to return the dashboard page. """

    profile = get_object_or_404(UserProfile, user=request.user)
    template = "home/dashboard.html"
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
    }

    return render(request, template, context)