
import random
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
)
from .forms import CardCheckForm

from .models import FlashCardSetList
from .models import Card


class FlashCardSetListView(ListView):
    model = FlashCardSetList
    template_name = "sets/index.html"
    # queryset = FlashCardSetList.objects.all().order_by("name")

class FlashCardSetCreateView(CreateView):
    model = FlashCardSetList
    template_name = "sets/sets_form.html"
    fields = ["name", "description"]
    success_url = reverse_lazy("index")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Add a new flashcard set"
        return context
    

class FlashCardSetDeleteView(DeleteView):
    model = FlashCardSetList
    template_name = "sets/sets_confirm_delete.html"
    success_url = reverse_lazy("index")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["flashcards_set"] = FlashCardSetList.objects.get(id=self.kwargs["pk"])
        context["set_id"] = self.kwargs["pk"]  # Add set_id to context
        return context


class CardListView(ListView):
    model = Card
    
    def get_queryset(self):
        set_id = self.kwargs['set_id']
        flashcard_set = get_object_or_404(FlashCardSetList, id=set_id)
        return Card.objects.filter(flashcard_set=flashcard_set).all().order_by("box", "-date_created")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        set_id = self.kwargs['set_id']
        flashcard_set = get_object_or_404(FlashCardSetList, id=set_id)
        context["flashcards_set"] = flashcard_set
        context["flashcard_set_name"] = flashcard_set.name
        context["set_id"] = set_id
        return context
    

class CardCreateView(CreateView):
    model = Card
    fields = ["question", "answer", "box"]
    
    def form_valid(self, form):
        set_id = self.kwargs['set_id']
        flashcard_set = get_object_or_404(FlashCardSetList, id=set_id)
        form.instance.flashcard_set = flashcard_set
        return super().form_valid(form)

    def get_context_data(self):
        context = super().get_context_data()
        context["set_id"] = self.kwargs["set_id"]  # Add set_id to context
        return context
    
    def get_success_url(self):
        return reverse_lazy("card-create", kwargs={'set_id': self.kwargs['set_id']})
    
    
class CardUpdateView(CardCreateView, UpdateView):
    model = Card
    
    def get_success_url(self):
        return reverse_lazy("card-list", kwargs={'set_id': self.kwargs['set_id']})

    def get_queryset(self):
        set_id = self.kwargs['set_id']
        flashcard_set = get_object_or_404(FlashCardSetList, id=set_id)
        return Card.objects.filter(flashcard_set=flashcard_set)


class CardDeleteView(DeleteView):
    model = Card

    def get_success_url(self):
        return reverse_lazy("card-list", kwargs={'set_id': self.kwargs['set_id']})

    def get_queryset(self):
        set_id = self.kwargs['set_id']
        flashcard_set = get_object_or_404(FlashCardSetList, id=set_id)
        return Card.objects.filter(flashcard_set=flashcard_set)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        set_id = self.kwargs['set_id']
        context["set_id"] = set_id  # Add set_id to context
        return context


class BoxView(CardListView):
    template_name = "cards/box.html"
    form_class =CardCheckForm
    
    def get_queryset(self):
        set_id = self.kwargs['set_id']
        flashcard_set = get_object_or_404(FlashCardSetList, id=set_id)
        return Card.objects.filter(flashcard_set=flashcard_set, box=self.kwargs["box_num"])
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args,**kwargs)
        context["box_number"] = self.kwargs["box_num"]
        context['set_id'] = self.kwargs['set_id']
        if self.object_list:
            context["check_card"] = random.choice(self.object_list)
        return context
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            card = get_object_or_404(Card, id=form.cleaned_data["card_id"])
            card.move(form.cleaned_data["solved"])
            
        return redirect(request.META.get("HTTP_REFERER"))

