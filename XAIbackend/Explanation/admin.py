from django.contrib import admin

from .models import Explanation


@admin.register(Explanation)
class ExplanationAdmin(admin.ModelAdmin):
    list_display = ("id", "query", "explainaing_algo", "explanation_type", "rating")
    search_fields = ("id", "explainaing_algo", "explanation_type")
    list_select_related = ("query",)
