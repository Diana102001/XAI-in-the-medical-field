from django import forms
from django.core.validators import FileExtensionValidator
from django.forms import formset_factory

from .models import AIModel


class InputFieldForm(forms.Form):
    FIELD_TYPES = [
        ("int", "Integer"),
        ("float", "Float"),
        ("long", "Long"),
        ("double", "Double"),
        ("string", "String"),
        ("boolean", "Boolean"),
        ("datetime", "Datetime"),
        ("image", "Image"),
        ("video", "Video"),
    ]

    name = forms.CharField(max_length=100)
    type = forms.ChoiceField(choices=FIELD_TYPES)
    required = forms.BooleanField(required=False)
    min_value = forms.FloatField(required=False)
    max_value = forms.FloatField(required=False)
    data_type = forms.CharField(max_length=100, required=False)
    batch_size = forms.IntegerField(required=False)
    rgb = forms.BooleanField(required=False)
    width = forms.IntegerField(required=False)
    height = forms.IntegerField(required=False)
    num_channels = forms.IntegerField(required=False)
    num_frames = forms.IntegerField(required=False)


class OutputFieldForm(InputFieldForm):
    pass


InputFieldFormSet = formset_factory(InputFieldForm, extra=1, can_delete=True)
OutputFieldFormSet = formset_factory(OutputFieldForm, extra=1, can_delete=True)


class AIModelForm(forms.Form):
    FLAVORS = [
        ("pytorch", "PyTorch"),
        ("keras", "Keras"),
    ]

    SOURCE_TYPE_CHOICES = [
        ("code", "Code and Enter Text"),
        ("file", "File and Submit File"),
    ]

    name = forms.CharField(max_length=255)
    dataset = forms.FileField(
        required=False,
        validators=[FileExtensionValidator(allowed_extensions=["csv"])],
        help_text="Upload a CSV file.",
    )
    classification_type = forms.ChoiceField(choices=AIModel.ClassificationType.choices)
    flavor = forms.ChoiceField(choices=FLAVORS)
    num_labels = forms.IntegerField(required=False)
    min_labels = forms.IntegerField(required=False)
    max_labels = forms.IntegerField(required=False)
    label_names = forms.CharField(widget=forms.HiddenInput(), required=False)
    source_type = forms.ChoiceField(choices=SOURCE_TYPE_CHOICES, widget=forms.RadioSelect)
    code_snippet = forms.CharField(widget=forms.Textarea, required=False)
    file = forms.FileField(required=False)
