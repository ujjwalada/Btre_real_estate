from django.urls import path

from . import views
#
urlpatterns = [
    path('', views.index, name='listings'),
    path('<int:list_id>', views.listing, name='list'),
    path('search', views.search, name='search'),
]
