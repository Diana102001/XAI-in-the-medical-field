from django.shortcuts import get_object_or_404
from .models import AIModel
import mlflow

class AIModelSingleton:
    _instances = {}

    @classmethod
    def get_model(cls, model_id):
        if model_id not in cls._instances:
            model = cls.load_model(model_id)  # Replace with your model loading logic
            cls._instances[model_id] = model
        return cls._instances[model_id]

    @staticmethod
    def load_model(model_id):
        aimodel= get_object_or_404(AIModel, id=model_id)
        uri=aimodel.modelURI
        flavor=aimodel.flavor
        flavor_module = getattr(mlflow, flavor)
        loaded_model_method = getattr(flavor_module, 'load_model')
        m=loaded_model_method(uri)
        return m