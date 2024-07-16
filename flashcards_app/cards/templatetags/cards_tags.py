# cards/templatetags/cards_tags.py

from django import template
from django.shortcuts import get_object_or_404
from cards.models import BOXES, Card, FlashCardSetList

register = template.Library()

@register.inclusion_tag("cards/box_links.html")
def boxes_as_links(set_id):
    boxes = []
    flashcard_set = get_object_or_404(FlashCardSetList, id=set_id)
    for box_num in BOXES:
        card_count =  Card.objects.filter(flashcard_set=flashcard_set, box=box_num).count()
        boxes.append({
            "number": box_num,
            "card_count": card_count,
            "set_id": set_id,
        })
        
    return {"boxes": boxes}