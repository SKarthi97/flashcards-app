from django.db import models


NUM_BOXES = 5
BOXES = range(1, NUM_BOXES + 1)

# word-to-word translations in the flashcards app
class Card(models.Model):

    question = models.CharField(max_length=100)
    answer = models.CharField(max_length=100)
    # keep track of the box number where the card sits.
    box = models.IntegerField(
        choices=zip(BOXES, BOXES), # with choices, make sure that the integer must contain a number that's within the boxes range.
        default=BOXES[0],
    )
    date_created = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return self.question

