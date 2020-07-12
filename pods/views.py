from django.shortcuts import render
from .models import Podcast

def pods(request):
    """ A view to return the Pods page """
    form = Podcast
    context = {
        'form': form,
    }
    return render(request, 'pods/pods.html', context)