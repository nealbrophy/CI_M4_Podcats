from django.shortcuts import render


def upgrade(request):
    """ A review to return the pro page. """

    return render(request, "pro/upgrade.html")