from django.urls import path
from . import views
app_name = "encyclopedia"

urlpatterns = [
    path("", views.index, name="index"),
    path ("wiki/<str:entry>", views.page, name="page"),
    path("search/", views.search, name="search"),
    path("new/", views.create, name="create"),
    path("check/", views.check, name="checker"),
    path("edit/<str:entry>", views.edit, name="edit"),
    path("changes/<str:entry>", views.changes, name="changes"),
    path("random/", views.randomPage, name="random"),
]
