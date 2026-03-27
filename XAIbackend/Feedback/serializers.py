from rest_framework import serializers

from .models import Feedback


class FeedbackSerializer(serializers.ModelSerializer):
    questions = serializers.SerializerMethodField()

    class Meta:
        model = Feedback
        fields = ["query", "star_ratings", "text_feedback", "questions"]

    def get_questions(self, obj):
        return Feedback.get_rating_questions()
