
from django.urls import path

from . import views


urlpatterns = [
    path(
        "",
        views.FlashCardSetListView.as_view(),
        name="index"
    ),
    path(
        "set/new",
        views.FlashCardSetCreateView.as_view(),
        name="flash-card-set-add"
    ),
    path(
        "set/<int:pk>/delete",
        views.FlashCardSetDeleteView.as_view(),
        name="flash-card-set-delete"
    ),
    path(
        "set/<int:set_id>/",
        views.CardListView.as_view(),
        name="card-list"
    ),
    path(
        "set/<int:set_id>/new",
        views.CardCreateView.as_view(),
        name="card-create"
    ),
    path(
        "set/<int:set_id>/edit/<int:pk>",
        views.CardUpdateView.as_view(),
        name="card-update"
    ),
    path(
        "set/<int:set_id>/box/<int:box_num>",
        views.BoxView.as_view(),
        name="box"
    ),
    path(
        "set/<int:set_id>/delete/<int:pk>",
        views.CardDeleteView.as_view(),
        name="card-delete"
    ),
]
