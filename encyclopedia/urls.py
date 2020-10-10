from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.title, name="title"),
    path("add", views.add, name="add"),
    path("random", views.random_select, name="random"),
    path("edit", views.edit, name="edit"),
    path("edit_page", views.edit_page, name="edit_page"),
    path("search", views.search, name="search")
]