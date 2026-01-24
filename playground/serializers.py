from rest_framework import serializers
from .models import AIModel,Query,Explanation,Feedback,Chat
from django import forms

class AIModelSerializer(serializers.ModelSerializer):
    class Meta:
        model=AIModel
        fields = '__all__'
    
class QuerySerializer(serializers.ModelSerializer):
    model = serializers.PrimaryKeyRelatedField(queryset=AIModel.objects.all())
    user = serializers.PrimaryKeyRelatedField(queryset=AIModel.objects.all())
    class Meta:
        model = Query
        fields = '__all__'

    # def validate(self, data):
    #     model = data.get('model')

    #     # if not ModelVersion.objects.filter(id=modelv.id, model_id=model.id).exists():
    #         # raise serializers.ValidationError("Selected model version is not associated with the selected AI model.")
        
    #     return data

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['model'] = instance.model.pk
        return ret
   
class ExplanationSerializer(serializers.ModelSerializer):
    class Meta:
        model=Explanation
        fields = '__all__'

########
class ExplanationRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Explanation
        fields = ['rating']


class DynamicFormSerializer(serializers.Serializer):
    # Dynamically add fields based on feature names
    def __init__(self, *args, **kwargs):
        feature_names = kwargs.pop('feature_names', None)
        super(DynamicFormSerializer, self).__init__(*args, **kwargs)
        if feature_names:
            for feature in feature_names:
                self.fields[feature] = serializers.CharField()

def serialize_form(form):
    form_data = {}
    for field_name, field in form.fields.items():
        bound_field = form[field_name]
        widget = bound_field.field.widget

        # Determine the type of input
        widget_type = widget.__class__.__name__
        input_type = widget.input_type if hasattr(widget, 'input_type') else 'text'

        # Prepare the field data dictionary
        field_data = {
            'type': input_type,
            'label': bound_field.label,
            'required': bound_field.field.required,
            'name': bound_field.html_name,
            'help_text': bound_field.help_text,
            'attrs': widget.attrs,
            # 'value': bound_field.value() if bound_field.is_bound else None,
            # 'errors': list(bound_field.errors) if bound_field.is_bound else None,
        }

        # Special handling for file input fields
        if isinstance(widget, forms.FileInput):
            field_data['attrs']['accept'] = widget.attrs.get('accept', 'image/*')

        form_data[field_name] = field_data
    
    return form_data

from rest_framework import serializers
from .models import Feedback

class FeedbackSerializer(serializers.ModelSerializer):
    questions = serializers.SerializerMethodField()

    class Meta:
        model = Feedback
        fields = ['query', 'star_ratings', 'text_feedback', 'questions']

    def get_questions(self, obj):
        return Feedback.get_rating_questions()


class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = ['id', 'query', 'user', 'sent_message', 'received_message', 'created_at']