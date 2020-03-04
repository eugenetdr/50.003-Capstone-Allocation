from django.urls import path

from . import views

urlpatterns = [
	# ex: /admin/
    path('', views.index, name='index'),
    # ex: /admin/floorplan/
    path('floorplan/', views.floorplan, name='floorplan'),
    # ex: /admin/floorplan/aprrove
    path('floorplan/confirmation/', views.approveConfirmation, name='approve'),
    # ex: /admin/floorplan/edit
    path('floorplan/edit/', views.editAllocation, name='edit'),
    # ex: /admin/floorplan/requirements
    path('floorplan/requirements/', views.viewRequirements, name='requirements'),
]