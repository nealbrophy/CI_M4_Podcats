from django.shortcuts import render


def upgrade(request):
    """ A review to return the pro page. """

    context = {
        "stripe_public_key": "pk_test_51GwAMXHTAoCBcf2ymYxl3YLq4QePvZxEQWcPzyt6Ei3ZyYSa0XXRfm3W16T7q5ZH3SR81ptvMuy4G0Pyt4LfF8Dc00PcEOy9D9",
        "client_secret": "test client secret",
    }

    return render(request, "pro/upgrade.html", context)


def benefits(request):
    """ A review to return the benefits page. """

    return render(request, "pro/benefits.html")