from django import forms
from django.contrib.auth import get_user_model
from rest_framework import serializers

from AIModel.models import AIModel
from .models import Query


class QuerySerializer(serializers.ModelSerializer):
    model = serializers.PrimaryKeyRelatedField(queryset=AIModel.objects.all())
    user = serializers.PrimaryKeyRelatedField(queryset=get_user_model().objects.all())

    class Meta:
        model = Query
        fields = "__all__"

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret["model"] = instance.model.pk
        return ret


class DynamicFormSerializer(serializers.Serializer):
    def __init__(self, *args, **kwargs):
        feature_names = kwargs.pop("feature_names", None)
        super().__init__(*args, **kwargs)
        if feature_names:
            for feature in feature_names:
                self.fields[feature] = serializers.CharField()


def serialize_form(form):
    form_data = {}
    for field_name, field in form.fields.items():
        bound_field = form[field_name]
        widget = bound_field.field.widget

        widget_type = widget.__class__.__name__
        input_type = widget.input_type if hasattr(widget, "input_type") else "text"

        field_data = {
            "type": input_type,
            "label": bound_field.label,
            "required": bound_field.field.required,
            "name": bound_field.html_name,
            "help_text": bound_field.help_text,
            "attrs": widget.attrs,
        }

        if isinstance(widget, forms.FileInput):
            field_data["attrs"]["accept"] = widget.attrs.get("accept", "image/*")

        form_data[field_name] = field_data

    return form_data
