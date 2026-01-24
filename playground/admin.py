from django.contrib import admin

# Register your models here.
from .models import AIModel,Query,Explanation,Feedback,Chat
admin.site.register(AIModel)
admin.site.register(Query)
admin.site.register(Feedback)
admin.site.register(Explanation)
admin.site.register(Chat)
