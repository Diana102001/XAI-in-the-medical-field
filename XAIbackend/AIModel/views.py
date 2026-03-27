from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
import json
import os
import pickle
import pandas as pd

from django.contrib.auth import get_user_model
from .models import AIModel
from .serializers import AIModelSerializer
from Query.models import Query


class AIModelViewSet(viewsets.ModelViewSet):
    queryset = AIModel.objects.all().order_by("-id")
    serializer_class = AIModelSerializer

    def create(self, request, *args, **kwargs):
        data_str = request.POST.get('data')
        if not data_str:
            return Response({"error": "No data provided"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            data = json.loads(data_str)
        except json.JSONDecodeError:
            return Response({"error": "Invalid JSON data"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Handle file if present
        model_file = request.FILES.get('file')
        if model_file and data.get('source_type') == 'file':
            # Save file logic here, similar to playground
            from django.core.files.storage import default_storage
            from django.conf import settings
            filepath = os.path.join(settings.MEDIA_ROOT, model_file.name)
            with default_storage.open(filepath, 'wb+') as destination:
                for chunk in model_file.chunks():
                    destination.write(chunk)
            data['modelURI'] = f"file://{filepath}"
        
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=True, methods=['get', 'post'], url_path='dynamic-form')
    def dynamic_form(self, request, pk=None):
        model = self.get_object()

        if request.method == 'GET':
            # Prefer input_signature from registered model if available.
            signature = model.input_signature or []
            form_fields = []
            if isinstance(signature, list):
                for field in signature:
                    form_fields.append({
                        'name': field.get('name'),
                        'label': field.get('name'),
                        'type': field.get('type', 'text'),
                        'required': field.get('required', False),
                        'attrs': {},
                    })
            return Response({'form': form_fields})

        # POST: model query
        input_data = request.data if isinstance(request.data, dict) else {}

        # Basic echo fallback if no model execution exists.
        prediction_result = {'echo': input_data}

        def resolve_uri(uri):
            if not uri:
                return None
            if uri.startswith('file://'):
                return uri[7:]
            return uri

        model_path = resolve_uri(model.modelURI)

        try:
            # handle direct pickle model path
            if model_path and model_path.lower().endswith('.pkl') and os.path.exists(model_path):
                with open(model_path, 'rb') as f:
                    loaded_model = pickle.load(f)

                if isinstance(input_data, dict):
                    dataframe_input = pd.DataFrame([input_data])
                else:
                    dataframe_input = input_data

                predict_raw = loaded_model.predict(dataframe_input)
                try:
                    predict_value = predict_raw.tolist() if hasattr(predict_raw, 'tolist') else predict_raw
                except Exception:
                    predict_value = str(predict_raw)

                prediction_result = {'result': predict_value}

            elif model.modelURI and model.modelURI.startswith('local://'):
                prediction_result = {'result': {'message': 'local model placeholder used; no MLflow artifact loaded', 'input': input_data}}

            elif model.flavor.lower() == 'pytorch':
                from .flavors.pytorch import pytorch
                flavor_instance = pytorch()
                raw_output = flavor_instance.useModel(input_data, model.modelURI)

                if hasattr(raw_output, 'detach'):
                    value = raw_output.detach().cpu().numpy().tolist()
                else:
                    value = raw_output

                prediction_result = {'result': value}

            elif model.flavor.lower() == 'keras':
                from .flavors.keras import Keras
                flavor_instance = Keras()
                raw_output = flavor_instance.useModel(input_data, model.modelURI)

                try:
                    value = raw_output.tolist() if hasattr(raw_output, 'tolist') else raw_output
                except Exception:
                    value = raw_output

                prediction_result = {'result': value}

            else:
                prediction_result = {'echo': input_data}

        except Exception as e:
            prediction_result = {
                'error': f'Prediction failed: {str(e)}',
                'echo': input_data,
            }

        # Save query to DB
        try:
            user_model = get_user_model()
            user = request.user if request.user.is_authenticated else user_model.objects.first()
            if user:
                Query.objects.create(
                    user=user,
                    model=model,
                    query_input=input_data,
                    query_output=prediction_result,
                )
        except Exception as e:
            # non-fatal: continue returning result
            print('Query save failed:', e)

        return Response({'result': prediction_result})

