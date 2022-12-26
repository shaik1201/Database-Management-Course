from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('Query_results', views.Query_results, name='Query_results'),
    path('add_movie', views.add_movie, name='add_movie')

]