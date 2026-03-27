from django.contrib import admin

from .models import Query


@admin.register(Query)
class QueryAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "model", "created_at")
    search_fields = ("id",)
    list_select_related = ("user", "model")
