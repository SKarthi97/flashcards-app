from django.db import models


NUM_BOXES = 5
BOXES = range(1, NUM_BOXES + 1)

class FlashCardSetList(models.Model):
    
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)  # Add this field
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("card-list", args=[self.id])

# word-to-word translations in the flashcards app
class Card(models.Model):

    question = models.CharField(max_length=100)
    answer = models.CharField(max_length=100)
    # keep track of the box number where the card sits.
    box = models.IntegerField(
        choices=zip(BOXES, BOXES), # with choices, make sure that the integer must contain a number that's within the boxes range.
        default=BOXES[0],
    )
    flashcard_set = models.ForeignKey(FlashCardSetList, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse(
            "card-create", args=[str(self.flashcard_set.id), str(self.id)]
        )
    
    def __str__(self):
        return self.question

    # To replicate the behavior of moving a card between boxes
    def move(self, solved):
        new_box = self.box + 1 if solved else BOXES[0]
        
        if new_box in BOXES:
            self.box = new_box
            self.save()
            
        return self
