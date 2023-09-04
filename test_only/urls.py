from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("adminOnly/", views.admin_only, name="admin_only"),
    path("committeeOnly/", views.committee_only, name="committee_only"),
    path("reset/", views.reset, name="reset"),
    path("createUser/", views.create_user, name="create_user"),
]
