from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


def validate_rating_step(value):
    if value % 0.5 != 0:
        raise ValidationError("Rating must be in increments of 0.5.")


# Create your models here.
class Explanation(models.Model):
    query = models.ForeignKey(
        "Query.Query",
        on_delete=models.CASCADE,
        related_name="explanations",
    )
    explainaing_algo = models.CharField(max_length=100)
    explanation_type = models.CharField(max_length=100)
    explain_input = models.JSONField()
    explain_output = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    rating = models.FloatField(
        default=0,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(5.0),
            validate_rating_step,
        ],
    )

    def __str__(self):
        return f"Explanation {self.pk} for Query {self.query_id}"
