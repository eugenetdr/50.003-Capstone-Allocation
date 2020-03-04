from django.urls import path

from . import views

urlpatterns = [
	# ex: /mode/
    path('', views.index, name='index'),
]