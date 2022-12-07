from django.urls import path
from . import views

# every view needs to be connected to a html page.
# first param is for the html page, second is for connecting to the view.
urlpatterns = [
    path('', views.index, name='index'),
    path('input_processor', views.input_processor, name='input_processor')

]
