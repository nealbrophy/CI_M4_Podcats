import csv, io
from django.shortcuts import render


def reviews(request):
    return render(request, 'reviews/index.html')
