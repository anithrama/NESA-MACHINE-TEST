from django.urls import path

from . import views

urlpatterns = [
    path("", views.add_route, name="add_route"),
    path("delete-route/<int:route_id>/", views.delete_route, name="delete_route"),
    path("q1/", views.q1, name="q1"),
    path("q2/", views.q2, name="q2"),
    path("q3/", views.q3, name="q3"),
]
