from django.shortcuts import render, redirect,get_object_or_404
from django.http import HttpResponse,JsonResponse
from .models import AIModel,Query,Explanation
from .forms import AIModelForm,QueryForm
from django.template.loader import render_to_string
import pandas as pd
import json
from interpret import show,preserve,show_link
import os
from .serializers import AIModelSerializer,QuerySeralizer,DynamicFormSerializer
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import Http404
from rest_framework import mixins
from rest_framework import generics
from rest_framework import viewsets, status
from rest_framework.decorators import action
import mlflow
from django.conf import settings
mlflow.set_tracking_uri(settings.MLFLOW_TRACKING_URI)
import mlflow.sklearn
from django.shortcuts import render, redirect
from .forms import ModelUploadForm
import mlflow
import pickle
import requests
import tensorflow as tf
import subprocess
from .flavors.pytorch import pytorch
from mlflow.models import Model
from mlflow.types import Schema
from django import forms
import torchvision.transforms as transforms
import numpy as np
import torch
from .Explainers.LimeImage import lime_image

# new API
class AIModelList(generics.ListAPIView):
    queryset = AIModel.objects.all()
    serializer_class = AIModelSerializer

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



class DynamicFormAPIView(APIView):

    def get(self, request, modelid):
        mlflow.set_tracking_uri("http://127.0.0.1:5000")
        model = get_object_or_404(AIModel, id=modelid)
        model_info = Model.load(model.modelURI)
        
        # Get the signature from the model metadata
        signature = model_info.signature
        input_schema = signature.inputs
        feature_names = [col.name for col in input_schema]
        feature_types = [col.type for col in input_schema]
        feature_shapes = [col.shape for col in input_schema]
        
        DynamicFormClass = create_dynamic_form(feature_names, feature_types, feature_shapes)
        form = DynamicFormClass()
        
        # Serialize the form fields to return as a JSON response
        form_fields =serialize_form(form)
        print(form)
        print(form_fields)
        
        return Response({'form': form_fields})

    def post(self, request, modelid):
        mlflow.set_tracking_uri("http://127.0.0.1:5000")
        model = get_object_or_404(AIModel, id=modelid)
        model_info = Model.load(model.modelURI)
        
        # Get the signature from the model metadata
        signature = model_info.signature
        input_schema = signature.inputs
        feature_names = [col.name for col in input_schema]
        feature_types = [col.type for col in input_schema]
        feature_shapes = [col.shape for col in input_schema]
        
        DynamicFormClass = create_dynamic_form(feature_names, feature_types, feature_shapes)
        form = DynamicFormClass(request.data, request.FILES)
        image_path=""
        if form.is_valid():
            cleaned_data = form.cleaned_data
            input_data = {}
            for name, dtype, shape in zip(feature_names, feature_types, feature_shapes):
                if name == "input_image":
       
       
                    media_path = "playground\images"
                    os.makedirs(media_path, exist_ok=True)
                    image = cleaned_data.get(name)
                    # Define the full path for the uploaded image
                    image_path = os.path.join(media_path, image.name)   
                    with open(image_path, 'wb+') as destination:
                        for chunk in image.chunks():
                            destination.write(chunk)            
       
       
                    image = Image.open(cleaned_data.get(name)).convert('RGB')
                    preprocessed_image = preprocess_image2(image, shape)
                    input_data[name] = preprocessed_image
                else:
                    input_data[name] = cleaned_data.get(name)

            flavor_class_map = {
                'pytorch': pytorch,
                # Add other mappings here
            }

            flavor = 'pytorch'  # get it from the database in ai model don't forget
            flavorClass = flavor_class_map[flavor]
            flavorInstance = flavorClass()
            result = flavorInstance.useModel(input_data, model.modelURI)
            ## Adjust
            
            tensor_list = result.detach().numpy().tolist()
            json_data = json.dumps({'tensor': tensor_list})

            query = Query(model=model, query_input=image_path, query_output=json_data)
            query.save()
            
            return Response({'result': result}, status=status.HTTP_200_OK)
        else:
            return Response({'errors': form.errors}, status=status.HTTP_400_BAD_REQUEST)


# API 
class QueryList(generics.ListAPIView):
    queryset = Query.objects.all()
    serializer_class = QuerySeralizer

    
class QueryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset=Query.objects.all()
    serializer_class=QuerySeralizer

class QueryCreateView(generics.CreateAPIView):
    queryset = Query.objects.all()
    serializer_class = QuerySeralizer
  


class QueryExplanationAPIView(APIView):
    def get(self, request, query_id):
        query = get_object_or_404(Query, id=query_id)
        e = query.explain()
        explanation = describe_explanation(e)  # Assuming describe_explanation is a function you have defined
        exp=Explanation(
            query=query,
            explanation_type="self_expanatory",
            explain_input=query.query_output,
            rate=0,
            explain_output=explanation
        )
        exp.save()
        return Response({'explanation': explanation}, status=status.HTTP_200_OK)
        




#############################################################
#############################################################
#############################################################
#############################################################
#############################################################
#############################################################
#############################################################
#############################################################
#############################################################
#############################################################
# Create your views here

def home(request):
    aimodels=AIModel.objects.all()
    context={'aimodels':aimodels}
    return render(request,"home.html",context)

def createAIModel(request):
    form=AIModelForm()
    if request.method == 'POST':
        form=AIModelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    context={'form':form}
    return render(request,'aimodel_form.html',context)


##############################################



def query_view(request):
    if request.method == 'POST':
        form = QueryForm(request.POST)
        if form.is_valid():
            model = form.cleaned_data['model']
            return redirect('dynamic_form_view', modelid=model.id)
    else:
        form = QueryForm()

    return render(request, 'query_form.html', {'form': form})

def get_field_by_type(name, dtype, shape=None):
    if not shape==None:
        field =forms.ImageField(label=name)
    elif dtype == "float32":
        field = forms.FloatField(label=name)
    elif dtype == "int32":
        field = forms.IntegerField(label=name)
    elif dtype == "string":
        field = forms.CharField(label=name)
    else:
        field = forms.CharField(label=name)  # default case
    return field

def create_dynamic_form(feature_names, feature_types, feature_shapes):
    class DynamicForm(forms.Form):
        pass

    for name, dtype, shape in zip(feature_names, feature_types, feature_shapes):
        field = get_field_by_type(name, dtype, shape)
        DynamicForm.base_fields[name] = field
    
    return DynamicForm

# def dynamic_form_view(request, modelid):
#     mlflow.set_tracking_uri("http://127.0.0.1:5000")
#     model = get_object_or_404(AIModel, id=modelid)
#     model_info = Model.load(model.modelURI)
    
#     # Get the signature from the model metadata
#     signature = model_info.signature
#     input_schema: Schema = signature.inputs
#     feature_names = [col.name for col in input_schema]
#     feature_types = [col.type for col in input_schema]
#     feature_shapes= [col.shape for col in input_schema]
    
#     DynamicFormClass  = create_dynamic_form(feature_names,feature_types,feature_shapes)
#     if request.method == "POST":
#         form = DynamicFormClass(request.POST,request.FILES)
#         if form.is_valid():
#             cleaned_data = form.cleaned_data
#             # Example: Process form data with your AI model
#             input_data = {}
#             for name, dtype, shape in zip(feature_names, feature_types, feature_shapes):
#                 if name=="input_image":
#                     print(dtype)
#                     image=Image.open(cleaned_data.get(name)).convert('RGB')
#                     preprocessed_image=preprocess_image2(image,shape)
#                     input_data[name]=preprocessed_image
#                 else:
#                     input_data[name] = cleaned_data.get(name)

#             # from model flavor create instance and return the model :)
#             flavor_class_map = {
#                 'pytorch': pytorch,
#                 # Add other mappings here
#             }
            
#             flavor='pytorch' # get it from database in ai model dooooon't forget
#             flavorClass = flavor_class_map[flavor]
#             flavorInstance=flavorClass()
#             result=flavorInstance.useModel(input_data,model.modelURI)
#             query=Query(model=model,query_input=json.dumps(input_data),query_output=json.dumps(result))
#             query.save()

#             return render(request, 'result_template.html', {'result': result})
#     else:
#         form = DynamicFormClass()
    
#     return render(request, 'dynamic_form.html', {'form': form})

  
from PIL import Image

def preprocess_image(img,shape):
    _,c,h,w=shape

    if (c==3):
       img = img.convert('RGB')
    else:
        img = img.convert('L') 
    preprocess = transforms.Compose([
        transforms.Resize(h,w),         # Resize to 256x256 pixels
        # transforms.CenterCrop(224),     # Crop the center 224x224 pixels
        transforms.ToTensor(),          # Convert to tensor
        transforms.Normalize(
             mean=[0.485, 0.456, 0.406],  # Normalize using ImageNet statistics
             std=[0.229, 0.224, 0.225]
        )
    ])
    
    # Open the image file
    img = preprocess(img)  # Apply the preprocessing steps
    image_np = img.numpy()
    t=torch.Tensor([image_np])
    return t


def preprocess_image2(image,shape):
    preprocess = transforms.Compose([
        transforms.Resize(256),         # Resize to 256x256 pixels
        transforms.CenterCrop(224),     # Crop the center 224x224 pixels
        transforms.ToTensor(),          # Convert to tensor
        transforms.Normalize(
            mean=[0.485, 0.456, 0.406],  # Normalize using ImageNet statistics
            std=[0.229, 0.224, 0.225]
        )
    ])
    
    img=image.convert('RGB')
    img = preprocess(img)  # Apply the preprocessing steps
    image_np = img.numpy()
    t=torch.Tensor([image_np])
    return t


def use_ai_model(model, input_data):
    # image=preprocess_image(input_data)
    # image_np = image.numpy()
    # t=torch.Tensor([image_np])
    result=model(input_data) 
    return {"result": result}

############# explain

def explain_query(request, query_id):
    query = get_object_or_404(Query, id=query_id)
    e = query.explain()
    explanation=describe_explanation(e)
    # explanation ="ccc"
    return JsonResponse({'explanation': explanation})


def describe_explanation(e):
    decision=(e._internal_obj.get('specific')[0]).get('decision')
    pre=(e._internal_obj.get('specific')[0]).get('perf').get('predicted_score')
    TheExp="The decision was made with these steps: from node "
    for d in decision:
        if (d==decision[-1]):
            TheExp+=str(d)+", so the taken decition is "+str(pre)+ " :)"
        else:
            nodes=(e._internal_obj.get('specific')[0]).get('nodes')
            for n in nodes:
                if (n.get('data').get('id')==str(d)):
                    f=n.get('data').get('label')
                    # Find the position of #
                    position_of_hash = f.find('#')
                    substring = f[:position_of_hash]
            TheExp+= str(d)+" the feature "+substring
            TheExp+=" then it goes to the node"
    
    return TheExp

def visualise_query(request, query_id):
    query = get_object_or_404(Query, id=query_id)
    e = query.explain()
    u=show_link(e)
    print(e)
    return redirect(u)



#################### MLFlow

from django.shortcuts import render, redirect
from .forms import ModelUploadForm, FieldForm,InputFieldFormSet

def upload_model(request):
    if request.method == 'POST':
        form = ModelUploadForm(request.POST, request.FILES)
        inputformset = InputFieldFormSet(request.POST)
        outputformset = InputFieldFormSet(request.POST)


        if form.is_valid() and inputformset.is_valid():
            flavor_class_map = {
                'pytorch': pytorch,
                # Add other mappings here
            }

            flavor = form.cleaned_data['flavor']
            name = form.cleaned_data['name']
            # source_file = form.cleaned_data['source_file']
            source_code = form.cleaned_data['source_code']
            
            flavor_class = flavor_class_map[flavor]
            flavor_instance = flavor_class(name=name)
            # get the input signature
            input_fields = [input_form.cleaned_data for input_form in inputformset]
            input_schema=GetSignature(input_fields)                 
            flavor_instance.inputSchema=input_schema
            # get the outbut signature
            output_fields = [outputform.cleaned_data for outputform in outputformset]
            output_schema=GetSignature(output_fields)
            flavor_instance.outputSchema=output_schema
            # add the code snippet
            flavor_instance.model=source_code
            # get model uri
            uri=flavor_instance.runCode()
            # create aimodel and save it
            aimodel=AIModel(modelURI=uri, name=name)
            aimodel.save()

            return redirect('success')  
    else:
        form = ModelUploadForm()
        formset = InputFieldFormSet()

    return render(request, 'upload.html', {'form': form, 'formset': formset})



def GetSignature(fields):
    input_schema="Schema(["
    for f in fields:
        field_name = f['field_name']
        field_type = f['field_type']
        is_required = f['is_required']
        if field_type=='image':
            # General attributes
            f['batch_size']
            f['data_type']
            # image
            f['image_channels']
            f['image_height']
            f['image_width']
            channels = 3 if f['is_rgb'] else 1
            input_schema+=f"TensorSpec(np.dtype(\"{f['data_type']}\"),({f['batch_size']},{channels},{f['image_height']},{f['image_width']}), \"{field_name}\"),"
        elif field_type=='video':
            # General attributes
            f['batch_size']
            f['data_type']
            # video
            f['video_channels']
            f['video_frames']
            f['video_height']
            f['video_width']
            input_schema+=f"TensorSpec(np.dtype(\"{f['data_type']}\"),({f['batch_size']},{f['video_channels']},{ f['video_frames']},{f['video_height']},{f['video_width']}), \"{field_name}\"),"
        elif field_type=='audio':
            # General attributes
            f['batch_size']
            f['data_type']
            # audio
            f['audio_channels']
            f['audio_samples']
            input_schema+=""
        else :
            input_schema+=f"TensorSpec(np.dtype(\"{f['data_type']}\"),({f['batch_size']},{ f['audio_channels']},{f['audio_samples']}), \"{field_name}\"),"

    input_schema=input_schema+"])"        


def explain_query(request, query_id):
    query = get_object_or_404(Query, id=query_id)
    inp=json.load(query.query_input)
    out=json.load(query.query_output)
    aimodel=query.model
    uri=aimodel.modelURI
    #if flavor is pytorch
    flavorclass=pytorch
    flavor=flavorclass()
    model = mlflow.pytorch.load_model(uri)
    #if input is image :)
    explainerclass=lime_image

    explainer=explainerclass()
    explanation=explainer.explaine(model,inp,out)
    result=processExplanation(explanation)  #how on earth we can generlize here :( => (AI model that generates the answer gpt or whatever :) )
    #json or sth :)
    return explanation


