from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('Query_results', views.Query_results, name='Query_results'),
    path('Rankings', views.Rankings, name='Rankings'),
    path('Records_management', views.Records_management, name='Records_management')

]