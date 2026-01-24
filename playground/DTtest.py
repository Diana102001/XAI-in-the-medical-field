# ml_utils.py

import os
import django
import pickle
import json
from django.shortcuts import get_object_or_404
from llamaapi import LlamaAPI
import numpy as np
from PIL import Image
from skimage.segmentation import mark_boundaries
import cv2

from playground.Explainers.LimeImage import LimeImage
# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'firstproject.settings')
django.setup()
from lime import lime_image
from .models import AIModel, Query, Explanation,User
from datetime import datetime
from sklearn.datasets import make_classification
import pandas as pd
from interpret.glassbox import (LogisticRegression,
                                ClassificationTree,
                                ExplainableBoostingClassifier)
from interpret.glassbox._decisiontree import TreeExplanation
from interpret import show
from sklearn.metrics import f1_score, accuracy_score
from sklearn.model_selection import train_test_split
from .serializers import AIModelSerializer
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
import io
from transformers import TFAutoModelForSequenceClassification
from tensorflow import keras
from huggingface_hub import hf_hub_download
import huggingface_hub as hub
from .ModelSingelton import AIModelSingleton

# from huggingface_hub import from_pretrained_keras
import mlflow
import mlflow.tensorflow
from sklearn.datasets import make_regression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split

import mlflow
import mlflow.sklearn
from mlflow.models import infer_signature
from transformers import AutoImageProcessor, AutoModelForImageClassification
from transformers import TFAutoModelForImageClassification, AutoFeatureExtractor
from huggingface_hub import hf_hub_download
import joblib
from torchsummary import summary
import torchvision.models as models
from .flavors.pytorch import pytorch
from .flavors.keras import Keras
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.resnet50 import preprocess_input, decode_predictions
import mlflow.pytorch
from mlflow.models import Model
from mlflow.types import Schema
import torchvision.transforms as transforms
import torch
from django import forms
import torch.nn.functional as F
from .Explainers.ExplainerFactory import ExplainerFactory
import requests
from tensorflow.keras.models import load_model
import tensorflow as tf
from .helpers import unique_filename,preprocess_image2

# model = joblib.load(hf_hub_download("osanseviero/wine-quality", "sklearn_model.joblib"))
# Load a pretrained ResNet model
model = models.resnet18(pretrained=True)

def preprocess_image(image_path):
    preprocess = transforms.Compose([
        transforms.Resize(256),         # Resize to 256x256 pixels
        transforms.CenterCrop(224),     # Crop the center 224x224 pixels
        transforms.ToTensor(),          # Convert to tensor
        transforms.Normalize(
            mean=[0.485, 0.456, 0.406],  # Normalize using ImageNet statistics
            std=[0.229, 0.224, 0.225]
        )
    ])
    
    # Open the image file
    img = Image.open(image_path).convert('RGB')  # Ensure 3 channels
    img = preprocess(img)  # Apply the preprocessing steps
    # img = img.unsqueeze(0)  # Add batch dimension

    return img
from skops.hub_utils import download
import tempfile
from huggingface_hub import hf_hub_url, cached_download
import cv2
from PIL import Image
import matplotlib.pyplot as plt # Import the pyplot module
import numpy as np
import mlflow
import mlflow.sklearn
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split


def run():

    print("hello")
    m=get_object_or_404(AIModel,id=1)
    print(m.input_signature)
    # # model = mlflow.keras.load_model("runs:/df42ab7c43e444a6850a8e4838b7b6f9/covid19")
    # # input=model.input
    # # print(input)
    # print("loaded 1")
    # metadata = mlflow.models.Model.load("runs:/df42ab7c43e444a6850a8e4838b7b6f9/covid19")
    # infp=mlflow.get_model_info("runs:/df42ab7c43e444a6850a8e4838b7b6f9/covid19")
    # print("loaded 2")
    # sig=metadata.signature.inputs
    # print(sig)

    # user=User(username="Fallola",password="Fallola")
    # user.save()
#     llama = LlamaAPI('LA-89511a0b5bae4468a37ece68d55bc174b6828d6d0afa40a4be41324d17b2a324')
#     api_request_json = {
#   "model": "llama3-70b",
#   "messages": [  
#     {"role": "system", "content": "You are a llama assistant that talks like a llama, starting every word with 'll'."},
#     {"role": "user", "content": "Hi, happy llama day!"},
#   ]
# }
    # Execute the Request
#     response = llama.run(api_request_json)
#     print(json.dumps(response.json(), indent=2))
# #     query=get_object_or_404(Query,id=11)
#     print(query.query_output)
    
    

#     conversation_history =[{"role": "system", "content": "you are going to be provided with input and labels say what is the diagnosis by mapping them in a short way"}]

#     def send_message_and_get_response(user_message):
#         # Append the user's message to the conversation history
#         conversation_history.append({"role": "user", "content": user_message})

#         # Prepare the request payload for the Llama API
#         api_request_json = {
#             "model": "llama3-70b",
#             "messages": conversation_history
#         }

#         # Execute the request to the Llama API
#         response = llama.run(api_request_json)
        
#         # Extract the bot's response from the API response
#         jsonres = response.json()
#         bot_response_content=jsonres['choices'][0]['message']['content']

#         # Append the bot's response to the conversation history
#         conversation_history.append({"role": "bot", "content": bot_response_content})

#         # Return the bot's response
#         return bot_response_content

    # Example usage:

    # Send the first message
    
    # first_response = send_message_and_get_response("i entered an chest xray image this is the output [0,1] these are the lables [corona, normal] can you say the diagnosis")
    # print("Bot:", first_response)

    # # Send the second message while maintaining context
    # conversation_history.append({"role": "system", "content": "you are a doctor assistant who doesnt rephrase but say original things"})
    # second_response = send_message_and_get_response("what to do for her now?")
    # print("Bot:", second_response)

    # print(conversation_history)


######################################### Image description
    # from PIL import Image
    # from transformers import AutoProcessor, GitVisionModel

    # processor = AutoProcessor.from_pretrained("microsoft/git-base")
    # model = GitVisionModel.from_pretrained("microsoft/git-base")

    # url = "http://images.cocodataset.org/val2017/000000039769.jpg"
    # image = Image.open("E:\\firstproject\\overlay_image.jpg")

    # inputs = processor(images=image, return_tensors="pt")

    # outputs = model(**inputs)
    # last_hidden_state = outputs.last_hidden_state



















    # query=get_object_or_404(Query,id=1)
    # d,t=query.get_input_and_input_type()
    # print(d)
    # print(t)
    # lime=LimeImage()
    # m = mlflow.keras.load_model("runs:/0077ca211913401c9a07111f4b46b09a/covid19")
    # l=lime.explaine(m,d)
    # en=lime.describeImageExplanation(l)
    # print(lime.name)
    # print(en)
    
    # r=test_image.resize((224,224))
    # image_path = unique_filename("playground/COVID19(466).jpg")
    
    # preprocessed_image = preprocess_image2(test_image, (-1,3,224,224))
    # print(image_path)
    # print(r.size)
    # Save the image to the specified directory
    # transform_to_pil = transforms.ToPILImage()
    # pil_image = transform_to_pil(preprocessed_image[0])
    # pil_image.save(image_path)
    # transform = transforms.ToTensor()

    # Apply the transform to the image
    # tensor_image = transform(r)
    # image_np = tensor_image.numpy()

    # t=torch.Tensor([image_np])
    # rearranged_tensor = t.permute(0, 2, 3, 1)
    # t=Image.open("playground/COVID19(466).jpg")
    # tt=preprocess_image2(t,(224,224))
    # loaded_model = mlflow.keras.load_model("runs:/0077ca211913401c9a07111f4b46b09a/covid19")
    # output=loaded_model(tt)
    
    # print(output)

    # class_dict = {0:'COVID19',
    #            1:'NORMAL',
    #            2:'PNEUMONIA'}
    # pred_class = np.argmax(output)
    # pred_class = class_dict[pred_class]
    # print('prediction: ',pred_class)
    # user=User(username='fallola',password='fallola')
    # user.save()



    # factory = ExplainerFactory()

    # image_explainers = factory.create_explainers('image')
    # for explainer in image_explainers:
    #     print(explainer.explaine(loaded_model,test_image))

    
    # # Load the model
    # m="model = tf.keras.models.load_model('E:/firstproject/playground/covid_model.h5')"
    # name="name=\"Keraaa\""
    # inputSchema="Schema([TensorSpec(np.dtype('float32'), (-1, 3, 224, 224),\"input_image\")])"
    # outputSchema="Schema([TensorSpec(np.dtype('float32'), (1, 3))])"

    # K=Keras()
    # uri=K.runCode(name,m,inputSchema,outputSchema) 
    # print(uri)
    # aimodel=AIModel(name=name,modelURI=uri)
    # aimodel.save()
    # #################
    # test_image =cv2.imread("playground/COVID19(466).jpg")
    # test_image = cv2.resize(test_image, (224,224),interpolation=cv2.INTER_NEAREST)
    # test_image = np.expand_dims(test_image,axis=0)
    # output=K.useModel(test_image,uri)
    
    # class_dict = {0:'COVID19',
    #           1:'NORMAL',
    #           2:'PNEUMONIA'}
    
    # # probs = model.predict(test_image)
    # pred_class = np.argmax(output)

    # pred_class = class_dict[pred_class]

    # print('prediction: ',pred_class)

    # from lime import lime_image
    # from skimage.segmentation import mark_boundaries
    # test_image =cv2.imread("playground/COVID19(466).jpg")
    # test_image = cv2.resize(test_image, (224,224),interpolation=cv2.INTER_NEAREST)
    # # LimeImageExplainer
    # explainer = lime_image.LimeImageExplainer()
    # loaded_model = mlflow.keras.load_model(uri)
    # # Explain prediction
    # explanation=explainer.explain_instance(test_image, loaded_model.predict, top_labels=5, hide_color=0, num_samples=1000)
    # # Show explanation
    # temp, mask = explanation.get_image_and_mask(explanation.top_labels[0], positive_only=True, num_features=5, hide_rest=False)
    # overlay_image = mark_boundaries(temp, mask)
    # # Convert image from float64 to uint8 (required for OpenCV)
    # overlay_image = (overlay_image * 255).astype(np.uint8)
    # path='overlay_image.jpg'
    # cv2.imwrite(path, cv2.cvtColor(overlay_image, cv2.COLOR_RGB2BGR))


































    # mlflow.keras.log_model(model, "keras1")
    # Load model directly
    # from transformers import AutoImageProcessor, AutoModelForImageClassification

    # processor = AutoImageProcessor.from_pretrained("nickmuchi/vit-base-xray-pneumonia")
    # model = AutoModelForImageClassification.from_pretrained("nickmuchi/vit-base-xray-pneumonia")
    # impath="E:\\firstproject\\playground\\dataset-card.jpg"
    # img = Image.open(impath)
    # input=processor(img)
    # output=model(input)
    # print(output)
    
    # p=explainer.explaine(model,inputs,outputs)
    # print(p)
    # Load a pre-trained ResNet-18 model
    # model = models.resnet18(pretrained=True)
    # model.eval()  # Set model to evaluation mode

    # # Define a dummy input tensor to log the model (batch size 1, 3 channels, 224x224 image size)
    # dummy_input = torch.randn(1, 3, 224, 224)
    # dummy_input_np = dummy_input.numpy()
    # input_example = {'input_image': dummy_input_np}
    # with torch.no_grad():
    #     dummy_output = model(dummy_input)
    # dummy_output_np = dummy_output.numpy()
    # # signature = infer_signature(input_example, dummy_output_np)
    # print(signature)
    # Convert image from float64 to uint8 (required for OpenCV)
    

    # Log the model in MLflow
    # with mlflow.start_run() as run:
    #     # Log the model with a dummy input (you can log metrics and parameters as well)
    #     m=mlflow.pytorch.log_model(model, "resnet_model",input_example=input_example,signature=signature)
    #     model_uri = m.model_uri
    #     print(model_uri)

    #     loaded_model = mlflow.pytorch.load_model(model_uri)
    #     aimodel=AIModel(name="resnet_model",modelURI=model_uri)
    #     aimodel.save()
    #     model_info = Model.load(model_uri)
    #     sig=model_info.signature
        
    #     if sig is not None:
    #         input_schema: Schema = sig.inputs
    #         feature_types = [col.type for col in input_schema]
    #         feature_shape=[col.shape for col in input_schema]
        
    #         print(feature_types)
    #         print(feature_shape)

    #         # Example usage: Load an image and make predictions
    #     image_path = 'E:\\firstproject\\playground\\dataset-card.jpg'  # Replace with the path to your image
    #     image = preprocess_image(image_path)
    #     print("Preprocessed Image Shape:", image.shape)
    #         # Convert to numpy array and check shape
    #     image_np = image.numpy()
    #     t=torch.Tensor([image_np])

    #     output = loaded_model(t)
       
    #         # Print the predicted output
    #     print("The input is:",image_np.shape)
    #     print("The output is:",output)

        
    # m="model = models.resnet18(pretrained=True)"
    # name="name=\"resnetttt\""
    # inputSchema="Schema([TensorSpec(np.dtype('float32'), (-1, 3, 224, 224)),])"
    # outputSchema="Schema([TensorSpec(np.dtype('float32'), (-1, 1000))])"
    # p=pytorch(name,m,inputSchema,outputSchema)
    # uri=p.runCode() 
    # print(uri)
    # aimodel=AIModel(name=name,modelURI=uri)
    # aimodel.save()

    # loaded_model2 = mlflow.pyfunc.load_model(uri)
    # output2 = loaded_model2.predict(image_np)

        # Print the predicted output
    # print("The input is:",image_np.shape)
    # print("The output is:",output2.shape)



    # print("hello")
    # print("dynamic form is",dynamicform)
    #get uri
# Set the tracking URI if necessary
# mlflow.set_tracking_uri("your_tracking_uri")
    # with mlflow.start_run() as r:
    #     mlflow.sklearn.log_model(model,"wineQuality")
    #     m=mlflow.pytorch.log_model(model, "resnet18_model")    
    #     print(f"Run ID: {r.info.run_id}")

    # loaded_model = mlflow.pytorch.load_model(m.model_uri)
    # loaded_model.eval()
    # summary(loaded_model, (3, 224, 224))

"""
    # Database connection URI
    
    # Define experiment name
    experiment_name = "Database RandomForest Regression"
    mlflow.set_experiment(experiment_name)

    # Generate synthetic data for regression
    X, y = make_regression(n_features=4, n_informative=2, random_state=0, shuffle=False)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Set model parameters
    params = {"max_depth": 2, "random_state": 42}
    model = RandomForestRegressor(**params)

    # Train the model
    model.fit(X_train, y_train)

    # Infer the model signature
    y_pred = model.predict(X_test)
    signature = infer_signature(X_test, y_pred)

    # Start an MLflow run
    with mlflow.start_run() as run:
        # Log parameters and metrics using the MLflow APIs
        mlflow.log_params(params)
        mlflow.log_metrics({"mse": mean_squared_error(y_test, y_pred)})

        # Log the sklearn model and register it locally
        mlflow.sklearn.log_model(
            sk_model=model,
            artifact_path="sklearn-model",
            signature=signature,
            registered_model_name="sk-learn-random-forest-reg-model"
        )
"""
    
    # repo = "keras-io/TF_Decision_Trees"
    # model = from_pretrained_keras("keras-io/TF_Decision_Trees")
    # model=hub.HfApi().model_info(repo)

    # model_filename = "model.h5"  
    # model_path = hf_hub_download(repo_id=repo_id, filename=model_filename)
    # model = keras.models.load_model(repo_id)

    # print(model)
    # aimodel=AIModel(name="test2",description="none")
    # aimodel.save()

    # serializer = AIModelSerializer(aimodel)
    # d=serializer.data

    # content = JSONRenderer().render(serializer.data)
    # print(content)

    # stream=io.BytesIO(content)
    # data=JSONParser().parse(stream)
    # print(data)

    # serializer=AIModelSerializer(data=data)
    # print(serializer.is_valid())

    # print(serializer.validated_data)
    # serializer.save()


    # serializer = AIModelSerializer(AIModel.objects.all(), many=True)
    # print(serializer.data)

#     # Generate synthetic data
#     X, y = make_classification(n_samples=1000, n_features=4, n_classes=2, random_state=42)

#     # Split the data into training and testing sets
#     X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


    # tree = ClassificationTree()
    # tree.fit(X_train.astype(float), y_train.astype(float))
    # print("Training finished.")
    # y_pred = tree.predict(X_test.astype(float))
    # print(f"F1 Score {f1_score(y_test.astype(float), y_pred.astype(float), average='macro')}")
    # print(f"Accuracy {accuracy_score(y_test.astype(float), y_pred.astype(float))}")

#     m = AIModel.objects.get(id=1)
# ##    print(m.name)
#     ###create model version
#     serialized_instance = pickle.dumps(tree)
    # pickle_file_path = 'dt1.pkl'
    # with open(pickle_file_path, 'wb') as file:
    #     pickle.dump(tree, file)
    # mlflow.log_artifact(pickle_file_path,artifact_path="model")
#     modelv=ModelVersion(model=m,model_file=serialized_instance,version_number='V1',released_at=datetime.now(),notes='blah blah')

#     modelv.save()
#     print(modelv.get_deferred_fields())
#     ###

#     input=np.array([1, 2, 1, 5])
#     output=np.array(tree.predict(input))
    
#     print(output)
#     queryinput=json.dumps(input.tolist())
#     queryoutput=json.dumps(output.tolist())
#     print("they are jsonsss now")
#     query = Query(
#     model=m,
#     modelv=modelv,
#     query_input=queryinput,
#     query_output=queryoutput
#     )
#     query.save()
#     print(query)
#     print(query.pk)
#     e=tree.explain_local(input,output) 
#     print("the explaination is: ",str(e._internal_obj))
    
#     decision=(e._internal_obj.get('specific')[0]).get('decision')
#     pre=(e._internal_obj.get('specific')[0]).get('perf').get('predicted_score')
#     TheExp="The decision was made with these steps: from node "
#     for d in decision:
#         if (d==decision[-1]):
#             TheExp+=str(d)+", so the taken decition is "+str(pre)+ " :)"
#         else:
#             nodes=(e._internal_obj.get('specific')[0]).get('nodes')
#             for n in nodes:
#                 if (n.get('data').get('id')==str(d)):
#                     f=n.get('data').get('label')    

#             TheExp+= str(d)+" the feature "+f
#             TheExp+=" then it goes to the node"
    
#     print("dddddddddd",TheExp)
#     # show(e)
#     print(tree.feature_names_in_)
#     print(tree.feature_types_in_)
#     exp=query.explain()

#     print("ffffffff",exp)    
#     # Convert the explanation to a dictionary
    
#     pickled_object = pickle.dumps(exp)
#     un_pickled_object=pickle.loads(pickled_object)
#     print(un_pickled_object)

#     # d=e.__dict__
#     # print(e._internal_obj["overall"])
#     # j=json.dumps(e)
#     #print(d)

#     #show(e)

#     # print(f"Explanation saved")
#     # explainationObj=Explanation(
#     #     query=query,
#     #     explanation_type="self_expanatory",
#     #     explain_input=query.query_output,
#     #     rate=0,
#     #     explain_output=query.query_input
#     # )
#     # explainationObj.save()
#     # print("the exp is",explainationObj)
    
"""
    q=Query(input,tree,m)
    output=q.query_output

    e=Explanation(q)
    o=e.explain_output
 """


""""
{'overall': None, 'specific': [{'type': 'tree', 'features': ['feature_0000', 'feature_0001', 'feature_0002', 'feature_0003'],
                                'nodes': [{'data': {'id': '1', 'label': 'feature_0002 <= -0.07\n# Obs: 0, 0', 'feature': 'feature_0002'}}, 
                                            {'data': {'id': '2', 'label': 'feature_0002 <= -0.43\n# Obs: 0, 0', 'feature': 'feature_0002'}},
                                            {'data': {'id': '3', 'label': 'feature_0000 <= -1.81\n# Obs: 0, 0', 'feature': 'feature_0000'}},
                                            {'data': {'id': '4', 'label': 'Impurity: 0.41\n# Obs: 0, 0', 'feature': None}},
                                            {'data': {'id': '5', 'label': 'Impurity: 0.17\n# Obs: 0, 0', 'feature': None}},
                                            {'data': {'id': '6', 'label': 'feature_0000 <= -0.63\n# Obs: 0, 0', 'feature': 'feature_0000'}},
                                            {'data': {'id': '7', 'label': 'Impurity: 0.24\n# Obs: 0, 0', 'feature': None}},
                                            {'data': {'id': '8', 'label': 'Impurity: 0.40\n# Obs: 0, 0', 'feature': None}},
                                            {'data': {'id': '9', 'label': 'feature_0000 <= -0.09\n# Obs: 0, 0', 'feature': 'feature_0000'}},
                                            {'data': {'id': '10', 'label': 'feature_0000 <= -0.77\n# Obs: 0, 0', 'feature': 'feature_0000'}},
                                            {'data': {'id': '11', 'label': 'Impurity: 0.07\n# Obs: 0, 0', 'feature': None}},
                                            {'data': {'id': '12', 'label': 'Impurity: 0.50\n# Obs: 0, 0', 'feature': None}},
                                            {'data': {'id': '13', 'label': 'feature_0002 <= 0.03\n# Obs: 0, 0', 'feature': 'feature_0002'}},
                                            {'data': {'id': '14', 'label': 'Impurity: 0.28\n# Obs: 0, 0', 'feature': None}},
                                            {'data': {'id': '15', 'label': 'Impurity: 0.00\n# Obs: 0, 1', 'feature': None}}],
                                'edges': [{'data': {'source': '3', 'target': '4', 'edge_weight': 0.13125}},
                                          {'data': {'source': '3', 'target': '5', 'edge_weight': 6.6}},
                                          {'data': {'source': '6', 'target': '7', 'edge_weight': 0.525}},
                                          {'data': {'source': '6', 'target': '8', 'edge_weight': 0.54375}},
                                          {'data': {'source': '2', 'target': '3', 'edge_weight': 6.731249999999999}},
                                          {'data': {'source': '2', 'target': '6', 'edge_weight': 1.0687499999999999}},
                                          {'data': {'source': '10', 'target': '11', 'edge_weight': 2.00625}},
                                          {'data': {'source': '10', 'target': '12', 'edge_weight': 1.36875}},
                                          {'data': {'source': '13', 'target': '14', 'edge_weight': 0.11249999999999999}},
                                          {'data': {'source': '13', 'target': '15', 'edge_weight': 3.7125}},
                                          {'data': {'source': '9', 'target': '10', 'edge_weight': 3.375}},
                                          {'data': {'source': '9', 'target': '13', 'edge_weight': 3.825}},
                                          {'data': {'source': '1', 'target': '2', 'edge_weight': 7.800000000000001}},
                                          {'data': {'source': '1', 'target': '9', 'edge_weight': 7.199999999999999}}],
                                'decision': array([ 1, 9, 13, 15]),
                                'perf': {'is_classification': True, 'actual': nan, 'predicted': 1, 'actual_score': nan, 'predicted_score': 1.0}}]}
"""