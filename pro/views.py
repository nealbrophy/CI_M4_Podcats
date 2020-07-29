from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .models import Purchase
from .forms import PurchaseForm

def upgrade(request):
    """ A review to return the pro page. """
    user = User.objects.get(id=request.user.id)

    if user.userprofile.pro_user:
        messages.info(request, "You already have a Pro account! You rock!")
        profile = user.userprofile
        context = {
            "profile": profile,
        }
        return redirect('dashboard')
    else:
        form = PurchaseForm()

    context = {
        "stripe_public_key": "pk_test_51GwAMXHTAoCBcf2ymYxl3YLq4QePvZxEQWcPzyt6Ei3ZyYSa0XXRfm3W16T7q5ZH3SR81ptvMuy4G0Pyt4LfF8Dc00PcEOy9D9",
        "client_secret": "test client secret",
        "form": form,
        "user": user,
    }

    return render(request, "pro/upgrade.html", context)


def benefits(request):
    """ A review to return the benefits page. """

    return render(request, "pro/benefits.html")