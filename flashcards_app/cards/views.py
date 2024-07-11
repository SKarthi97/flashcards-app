
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    CreateView,
)


from .models import Card

class CardListView(ListView):
    model = Card
    queryset = Card.objects.all()

class CardCreateView(CreateView):
    model = Card
    fields = ["question", "answer", "box"]
    success_url = reverse_lazy("card-create")
