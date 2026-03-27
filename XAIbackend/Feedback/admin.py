from django.contrib import admin

from .models import Feedback


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ("id", "query", "created_at", "updated_at")
    search_fields = ("id",)
    list_select_related = ("query",)
