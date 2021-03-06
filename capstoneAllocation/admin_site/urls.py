from django.urls import path

from . import views

urlpatterns = [
	# ex: /admin/1/
    path('', views.index, name='adminIndex'),
    # ex: /admin/1/floorplan/
    path('<str:user>/<int:active>/floorplan/', views.floorplan, name='floorplan'),
    # ex: /admin/logout
    path('<str:user>/logout/', views.logout, name='logout'),
    # ex: /admin/1/floorplan/confirmation
    path('<str:user>/<int:active>/floorplan/confirmation/', views.approveConfirmation, name='approve'),
    # ex: /admin/1/floorplan/confirmation/aprrove
    path('<str:user>/<int:active>/floorplan/confirmation/approve', views.approve, name='confirm'),
    # ex: /admin/1/floorplan/edit
    path('<str:user>/<int:active>/floorplan/edit/', views.editAllocation, name='edit'),
    # ex: /admin/1/floorplan/sendFloorPlan1
    path('<str:user>/<int:active>/floorplan/saveAllocation1/', views.saveAllocation1, name='saveAllocation1'),
    # ex: /admin/1/floorplan/edit2
    path('<str:user>/<int:active>/floorplan/edit2/', views.editAllocation2, name='edit2'),
    # ex: /admin/1/floorplan/sendFloorPlan2
    path('<str:user>/<int:active>/floorplan/saveAllocation2/', views.saveAllocation2, name='saveAllocation2'),
    # ex: /admin/1/floorplan/requirements
    path('<str:user>/<int:active>/floorplan/requirements/', views.viewRequirements, name='requirements'),
    # ex: /admin/logout
    path('<str:user>/logout/', views.logout, name='logout'),
]