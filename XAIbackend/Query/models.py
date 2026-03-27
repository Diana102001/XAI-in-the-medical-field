from django.conf import settings
from django.db import models


# Create your models here.
class Query(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="queries",
    )
    model = models.ForeignKey(
        "AIModel.AIModel",
        on_delete=models.CASCADE,
        related_name="queries",
    )
    query_input = models.JSONField()
    query_output = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_input_and_input_type(self):
        from .services import parse_query_input

        return parse_query_input(self.query_input)

    def __str__(self):
        return f"Query {self.pk} for {self.model_id}"



