from django.urls import path

from . import views

urlpatterns = [
	# ex: /admin/1/
    path('', views.index, name='adminIndex'),
    # ex: /admin/1/floorplan/
    path('<str:user>/<int:active>/floorplan/', views.floorplan, name='floorplan'),
    # ex: /admin/1/floorplan/
    path('<str:user>/<int:active>/floorplan2/', views.floorplan2, name='floorplan2'),
    # ex: /admin/logout
    path('<str:user>/logout/', views.logout, name='logout'),
    # ex: /admin/1/floorplan/aprrove
    path('<str:user>/<int:active>/floorplan/confirmation/', views.approveConfirmation, name='approve'),
    # ex: /admin/1/floorplan/edit
    path('<str:user>/<int:active>/floorplan/edit/', views.editAllocation, name='edit'),
    # ex: /admin/1/floorplan/edit2
    path('<str:user>/<int:active>/floorplan/edit2/', views.editAllocation2, name='edit2'),
    # ex: /admin/1/floorplan/requirements
    path('<str:user>/<int:active>/floorplan/requirements/', views.viewRequirements, name='requirements'),
    # ex: /admin/logout
    path('<str:user>/logout/', views.logout, name='logout'),
]