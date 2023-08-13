
from django.shortcuts import get_object_or_404, render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.
from listings.choices import price_choices, bedroom_choices, state_choices

from .models import Listing


def index(request):
    listings = Listing.objects.order_by('-list_date').filter(is_published=True)
    paginator = Paginator(listings, 3)
    page = request.GET.get('page')
    paged_listings = paginator.get_page(page)

    context = {
        'listings': paged_listings
    }
    return render(request, 'listings/listings.html', context)


def listing(request, list_id):
    list1 = get_object_or_404(Listing, pk=list_id)
    context = {
        'l1': list1,
    }
    return render(request, 'listings/listing.html', context)


def search(request):
    queryset = Listing.objects.order_by('-list_date')

    # description
    if 'keywords' in request.GET:
        keywords = request.GET['keywords']
        if keywords:
            queryset = queryset.filter(description__icontains=keywords)

    # city based filteration
    if 'city' in request.GET:
        city = request.GET['city']
        if city:
            queryset = queryset.filter(city__iexact=city)

    # state based filteration
    if 'state' in request.GET:
        state = request.GET['state']
        if state:
            queryset = queryset.filter(state__iexact=state)

   # bedrooms based filteration
    if 'bedrooms' in request.GET:
        bedrooms = request.GET['bedrooms']
        if bedrooms:
            queryset = queryset.filter(bedrooms__lte=bedrooms)

    # price based filteration
    if 'price' in request.GET:
        price = request.GET['price']
        if price:
            queryset = queryset.filter(price__lte=price)

    context = {

        'state_choices': state_choices,
        'bedroom_choices': bedroom_choices,
        'price_choices': price_choices,
        'listings': queryset,
        'values': request.GET,

    }
    return render(request, 'listings/search.html', context)
