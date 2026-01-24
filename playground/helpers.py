from django import forms
import os
import uuid
from mlflow.models import Model
import mlflow
import torchvision.transforms as transforms
from django.shortcuts import render, redirect,get_object_or_404
import torch
from .models import AIModel
import json
import cv2
import numpy as np
from llamaapi import LlamaAPI

def get_field_by_type(name, dtype, shape=None):
    if  dtype=="image":###
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

def preprocess_image2(image,shape):
    image_np = np.array(image)
    # Convert RGB to BGR (OpenCV format)
    image_cv = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)
    image_cv = cv2.resize(image_cv, (224,224),interpolation=cv2.INTER_NEAREST)
    image_cv = np.expand_dims(image_cv,axis=0)
    return image_cv

def get_model_and_form(modelid, model_cache):
    if modelid not in model_cache:
        mlflow.set_tracking_uri("http://127.0.0.1:5000")
        model = get_object_or_404(AIModel, id=modelid)
        # model_info = Model.load(model.modelURI)
        
        # # Get the signature from the model metadata
        # signature = model_info.signature
        # input_schema = signature.inputs
        # feature_names = [col.name for col in input_schema]
        # feature_types = [col.type for col in input_schema]
        # feature_shapes = [col.shape for col in input_schema]
        feature_names=[]
        feature_types=[]
        feature_shapes=[]

        input_fields_json=model.input_signature
        input_fields=json.loads(input_fields_json)
        for field in input_fields:
           feature_names.append(field["name"]) 
           feature_types.append(field["type"])
           colors=1
           if field["rgb"]:
               colors=3
           shape=(field["batch_size"],colors,field["width"],field["height"])
           feature_shapes.append(shape)


        DynamicFormClass = create_dynamic_form(feature_names, feature_types, feature_shapes)
        model_cache[modelid] = (model, DynamicFormClass, feature_names, feature_types, feature_shapes)
    else:
        model, DynamicFormClass, feature_names, feature_types, feature_shapes = model_cache[modelid]
    
    return model, DynamicFormClass, feature_names, feature_types, feature_shapes

def unique_filename(filename):
    # Extract file extension
    ext = filename.split('.')[-1]
    # Generate unique file name
    unique_name = f"{uuid.uuid4().hex}.{ext}"
    return os.path.join('playground/images/', unique_name)

def toJson(obj):
    res=json.dumps(obj)
    return res


def GetSignature(fields):
    input_schema="Schema(["
    for f in fields:
        field_name = f['name']
        field_type = f['type']
        if f['required']==1:
            is_required = 'true'
        else: is_required="false"
        if field_type=='image':
            # General attributes
            f['batch_size']
            f['data_type']
            # image
            f['rgb']
            f['height']
            f['width']
            channels = 3 if f['rgb'] else 1
            input_schema+=f"TensorSpec(np.dtype(\"{f['data_type']}\"),({f['batch_size']},{channels},{f['height']},{f['width']}), \"{field_name}\"),"
        elif field_type=='video':
            # General attributes
            f['batch_size']
            f['data_type']
            # video
            f['num_channels']
            f['num_frames']
            f['width']
            f['height']
            input_schema+=f"TensorSpec(np.dtype(\"{f['data_type']}\"),({f['batch_size']},{f['video_channels']},{ f['video_frames']},{f['video_height']},{f['video_width']}), \"{field_name}\"),"
        # elif field_type=='audio':
        #     # General attributes
        #     f['batch_size']
        #     f['data_type']
        #     # audio
        #     f['audio_channels']
        #     f['audio_samples']
        #     input_schema+=""
        # else :
        #     input_schema+=f"TensorSpec(np.dtype(\"{f['data_type']}\"),({f['batch_size']},{ f['audio_channels']},{f['audio_samples']}), \"{field_name}\"),"
        else :
           input_schema+=f"ColSpec(\"{field_type}\",\"{field_name}\",\"{is_required}\"),"

    input_schema=input_schema+"])"
    return input_schema        



def send_message_and_get_response(conversation_history,user_message):
    llama = LlamaAPI('LL-5NjBsqPsddHc7Pom06EV5RZ3GeURk4qoaqvSzhsbOyXyjB77HQpZKb00QWlKIV8Z')
    # Append the user's message to the conversation history
    conversation_history.append({"role": "user", "content": user_message})
    # Prepare the request payload for the Llama API
    api_request_json = {
        "model": "llama3-70b",
        "messages": conversation_history
    }
    # Execute the request to the Llama API
    response = llama.run(api_request_json)
    
    # Extract the bot's response from the API response
    jsonres = response.json()
    bot_response_content=jsonres['choices'][0]['message']['content']
    # Append the bot's response to the conversation history
    conversation_history.append({"role": "bot", "content": bot_response_content})
    # Return the bot's response
    return bot_response_content
