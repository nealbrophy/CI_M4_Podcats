from django.shortcuts import render


def upgrade(request):
    """ A review to return the pro page. """

    return render(request, "pro/upgrade.html")


def benefits(request):
    """ A review to return the benefits page. """

    return render(request, "pro/benefits.html")