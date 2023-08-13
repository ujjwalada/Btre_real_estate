from django.http import HttpResponse
from django.shortcuts import render
from django.http import HttpResponse
from listings.choices import price_choices, bedroom_choices, state_choices
# Create your views here.

from listings.models import Listing

from realtors.models import Realtor


def index(request):
    listings = Listing.objects.order_by(
        '-list_date').filter(is_published=True)[:3]
    context = {
        'listings': listings,
        'state_choices': state_choices,
        'bedroom_choices': bedroom_choices,
        'price_choices': price_choices,

    }
    return render(request, 'pages/index.html', context)


def about(request):
    # get all realtor
    r1 = Realtor.objects.order_by('-hire_date')
    # get all MVP
    m1 = Realtor.objects.all().filter(is_nvp=True)

    context = {
        'real1': r1,
        'mvp': m1,
    }
    return render(request, 'pages/about.html', context)
