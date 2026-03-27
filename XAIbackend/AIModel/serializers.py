from rest_framework import serializers

from .models import AIModel


class AIModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = AIModel
        fields = "__all__"

    def validate_labels(self, value):
        # Accept labels as array or object for compatibility.
        if isinstance(value, list):
            return {
                "num_labels": len(value),
                "label_names": value,
                "min_labels": 1 if len(value) > 0 else 0,
                "max_labels": len(value),
            }

        if isinstance(value, dict):
            labels = dict(value)
            names = labels.get("label_names") or labels.get("labels") or []
            if not isinstance(names, list):
                raise serializers.ValidationError("label_names must be an array")

            labels.setdefault("num_labels", len(names))
            labels.setdefault("min_labels", 1 if len(names) > 0 else 0)
            labels.setdefault("max_labels", len(names))
            labels["label_names"] = names
            return labels

        raise serializers.ValidationError("Invalid labels format")
