
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    UpdateView,
)


from .models import Card

class CardListView(ListView):
    model = Card
    queryset = Card.objects.all().order_by("box", "-date_created")


class CardUpdateView(UpdateView):
    model = Card
    fields = ["question", "answer", "box"]
    success_url = reverse_lazy("card-list")
