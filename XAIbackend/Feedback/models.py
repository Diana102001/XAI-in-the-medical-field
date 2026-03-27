from django.db import models


# Create your models here.
class Feedback(models.Model):
    query = models.OneToOneField(
        "Query.Query",
        on_delete=models.CASCADE,
        related_name="feedback",
    )
    star_ratings = models.JSONField()
    text_feedback = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @staticmethod
    def get_rating_questions():
        return [
            "How well did the prediction meet your expectations?",
            "How much clearer did the explanations make the prediction?",
            "How confident are you in the prediction after reviewing the explanations?",
        ]

    def __str__(self):
        return f"Feedback for Query {self.query_id}"
