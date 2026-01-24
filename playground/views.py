from itertools import count
import os
from requests import Response
from sympy import Q
from playground.forms import AIModelForm,InputFieldFormSet,OutputFieldFormSet
from .models import AIModel,Query,Explanation,Feedback,User,Chat
from rest_framework import generics, status
from rest_framework.response import Response  # Correct Response import
from  .serializers import AIModelSerializer,serialize_form,FeedbackSerializer,ChatSerializer,ExplanationSerializer,QuerySerializer,ExplanationRatingSerializer
from rest_framework.views import APIView
from django.shortcuts import render, redirect,get_object_or_404
from PIL import Image
from .flavors.FlavorsFactory import FlavorsFactory
import torchvision.transforms as transforms
from .helpers import preprocess_image2,get_model_and_form, send_message_and_get_response,unique_filename,toJson,GetSignature
import json
from .Explainers.ExplainerFactory import ExplainerFactory
from django.http import JsonResponse
from llamaapi import LlamaAPI
from rest_framework.exceptions import ValidationError
from .ModelSingelton import AIModelSingleton
from django.core.files.storage import default_storage
from django.conf import settings
from datetime import datetime
import matplotlib.pyplot as plt
import io
import base64

# API
# get models (make sure of versioning)
class AIModelList(generics.ListAPIView):
    queryset = AIModel.objects.all()
    serializer_class = AIModelSerializer

# get dynamic form and prediction
class DynamicFormAPIView(APIView):

    model_cache = {}

    def get(self, request, modelid):
        model, DynamicFormClass, feature_names, feature_types, feature_shapes = get_model_and_form(modelid, self.model_cache)
        form = DynamicFormClass()
        
        # Serialize the form fields to return as a JSON response
        form_fields = serialize_form(form)
        return JsonResponse({'form': form_fields})
    
    def post(self, request, modelid):
        model, DynamicFormClass, feature_names, feature_types, feature_shapes = get_model_and_form(modelid, self.model_cache)
        form = DynamicFormClass(request.data, request.FILES)
        
        if form.is_valid():
            cleaned_data = form.cleaned_data
            input_data = {}
            input_data_jsonable={}
            for name, dtype, shape in zip(feature_names, feature_types, feature_shapes):
                if shape is not None:
                    # check if video or image or audio then deal with it :)
                    image = cleaned_data.get(name)
                    image_path = unique_filename(image.name)
                    image2 = Image.open(image).convert('RGB')
                    preprocessed_image = preprocess_image2(image2, shape)
                    input_data[name] = preprocessed_image
                    input_data_jsonable[name]=image_path
                    # Save the image to the specified directory
                    # with open(image_path, 'wb+') as destination:
                    #     for chunk in preprocessed_image.chunks():
                    #         destination.write(chunk)
                    transform_to_pil = transforms.ToPILImage()
                    pil_image = transform_to_pil(preprocessed_image[0])
                    pil_image.save(image_path)

                else:
                    input_data[name] = cleaned_data.get(name)
                    input_data_jsonable[name]=cleaned_data.get(name)

            flavorsFactory = FlavorsFactory()
            result = flavorsFactory.useModel(model,input_data) # AIModel (we can get flavor and uri :) )
            tensor_list = result.numpy().tolist()
            print(result)
            json_input = toJson(input_data_jsonable)
            # Convert list to JSON
            # tensor_json = json.dumps(tensor_list)
            json_result = toJson(tensor_list)
            user=User.objects.get(id=1)
            
            query = Query(user=user,model=model, query_input=json_input, query_output=json_result)
            query.save()
            # Save the query ID to use it for explanation
            request.session['last_query_id'] = query.id
            lables=json.loads(model.labels)["label_names"]
            
            
            ###Llama
            conv_hist=[{"role": "system", "content": "you are going to be provided with input and labels say what is the diagnosis by mapping them in humen understndable way"}]
            user_message="query output is"+query.query_output+" and query labels are "+str(lables)
            print(user_message)
            # potresponse=send_message_and_get_response(conv_hist,user_message)
            # return JsonResponse({'result': json_result, 'query_id': query.id})
            potresponse="the prediction is Normal"
            meassage=Chat(user=user,query=query,sent_message='Predict',received_message=potresponse)
            meassage.save()
            return JsonResponse({'result': potresponse, 'query_id': query.id})
            return JsonResponse({'result': query.query_output, 'query_id': query.id})
        else:
            return Response({'errors': form.errors}, status=status.HTTP_400_BAD_REQUEST)

# feedback
class FeedbackView(APIView):
    def get(self, request, query_id):
        try:
            feedback = Feedback.objects.get(query_id=query_id)
            serializer = FeedbackSerializer(feedback)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Feedback.DoesNotExist:
            # Even if feedback does not exist, return the questions
            questions = Feedback.get_rating_questions()
            return Response({"questions": questions}, status=status.HTTP_200_OK)

    def post(self, request, query_id):
        try:
            query = Query.objects.get(id=query_id)
            data = request.data.copy()
            data['query'] = query.id

            serializer = FeedbackSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Query.DoesNotExist:
            return Response({"error": "Query not found."}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, query_id):
        try:
            feedback = Feedback.objects.get(query_id=query_id)
            serializer = FeedbackSerializer(feedback, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Feedback.DoesNotExist:
            return Response({"error": "Feedback not found."}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, query_id):
        try:
            feedback = Feedback.objects.get(query_id=query_id)
            feedback.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Feedback.DoesNotExist:
            return Response({"error": "Feedback not found."}, status=status.HTTP_404_NOT_FOUND)


# explain
class ExplainAPIView(APIView):
    def get(self, request, modelid,query_id):
        # query_id = request.session.get('last_query_id')
        # if not query_id:
        #     return Response({'error': 'No query found for explanation.'}, status=status.HTTP_400_BAD_REQUEST)

        query = get_object_or_404(Query, id=query_id)
        input_data,input_type=query.get_input_and_input_type()
        AImodel=get_object_or_404(AIModel,id=modelid)
        flavorsFactory = FlavorsFactory()
        model=flavorsFactory.getModel(AImodel)

        explainers_factory=ExplainerFactory()
        # ex_type='image'
        explainers=explainers_factory.create_explainers(input_type)
        explanations={}
        explanation_ids = [] 
        # see how to get type
        for explainer in explainers:
            explanation=explainer.explaine(model,input_data)
            name=explainer.name
            # explanations[name]=explanation
            enhanced_exlpanation=explainer.describeImageExplanation(explanation)
            explanations[name]=enhanced_exlpanation
            exp=Explanation(query=query,explainaing_algo=name,explanation_type=input_type,explain_input={"non":0},explain_output=explanation)
            exp.save()
            explanation_ids.append(exp.id)
            user=User.objects.get(id=1)
            message=Chat(user=user,query=query,sent_message='Explain',received_message=enhanced_exlpanation)
            message.save()
        return JsonResponse({'explanation': explanations, 'explanation_ids': explanation_ids})

# rate explanation
class ExplanationRatingAPIView(generics.UpdateAPIView):
    queryset = Explanation.objects.all()
    serializer_class = ExplanationRatingSerializer
    # lookup_field = 'id'  # Add this line to specify the lookup field

    def update(self, request, *args, **kwargs):
        # explanation_id = kwargs.get('explanation_id')
        explanation = self.get_object()
        
        # Validate and update the rating
        serializer = self.get_serializer(explanation, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        return Response(serializer.data, status=status.HTTP_200_OK)

# get queries (login :))
class UserQueryListView(generics.ListAPIView):
    serializer_class = QuerySerializer
    # permission_classes = [IsAuthenticated]
    def get_queryset(self):
        user=User.objects.get(id=1)
        return Query.objects.filter(user=user).order_by('-created_at')



class ChatListView(generics.ListAPIView):
    serializer_class = ChatSerializer

    def get_queryset(self):
        query_id = self.kwargs['query_id']
        return Chat.objects.filter(query_id=query_id)
# chatbot
def chatbot(request):
    llama = LlamaAPI('LL-jlbVjI6hIDUrPqq5ssyHOW9lHKwZ0U50Pnp66zdEyuHfcDc56Tb5S9YZNeVmSTzB')

    if request.method == 'POST':
        user_input = request.POST.get('user_input')

        # If the user input contains form data
        if 'form_field_1' in request.POST:
            # Process form data here
            form_data_1 = request.POST.get('form_field_1')
            form_data_2 = request.POST.get('form_field_2')

            # Generate a response based on form data
            bot_response = f"Llama says: Thank you for providing {form_data_1} and {form_data_2}."

            return JsonResponse({'bot_response': bot_response})

        # Otherwise, continue with normal chat interaction
        api_request_json = {
            "model": "llama3-70b",
            "messages": [
                {"role": "system", "content": "You are a llama assistant"},
                {"role": "user", "content": user_input},
            ]
        }

        response = llama.run(api_request_json)
        jsonRes = response.json()
        ans = jsonRes['choices'][0]['message']['content']

        return JsonResponse({'bot_response': ans})

    # If it's a GET request, show the initial form
    return render(request, 'chatbot2.html')
       
# Admin 
# upload model
def upload_model(request):
    if request.method == 'POST':
        form = AIModelForm(request.POST)
        input_formset = InputFieldFormSet(request.POST, prefix='input')
        output_formset = OutputFieldFormSet(request.POST, prefix='output')

        if form.is_valid() and input_formset.is_valid() and output_formset.is_valid():
            classification_type = form.cleaned_data['classification_type']
            flavor = form.cleaned_data['flavor']
            name = form.cleaned_data['name']
            num_labels = form.cleaned_data['num_labels']
            min_labels = form.cleaned_data['min_labels']
            max_labels = form.cleaned_data['max_labels']
            
            # Process labels
            label_names = [request.POST.get(f'label_{i}') for i in range(num_labels) if request.POST.get(f'label_{i}')]
            labels = {
                "num_labels": num_labels,
                "label_names": label_names,
                "min_labels": min_labels,
                "max_labels": max_labels
            }
            print(labels)
            # Process input fields
            input_fields = [form.cleaned_data for form in input_formset]
            input_signature = GetSignature(input_fields)  # Assuming GetSignature is defined elsewhere
            print(input_fields)
            print(input_signature)

            # # Process output fields
            # output_fields = [form.cleaned_data for form in output_formset]
            # output_signature = GetSignature(output_fields)  # Assuming GetSignature is defined elsewhere

            output_signature="Schema([TensorSpec(np.dtype(\"float32\"),(-1,"+str(num_labels)+"), \"class\"),])"

            source_type = request.POST.get('source_type')
            if source_type == 'code':
                code_snippet = request.POST.get('code_snippet')
                flavorsFactory = FlavorsFactory()
                modelURI = flavorsFactory.upload_model(flavor, name, code_snippet, input_signature, output_signature)
                print("modelURIis",modelURI)
            # elif model_source == 'file':
            #     model_file = request.FILES.get('model_file')

                aimodel = AIModel(name=name, flavor=flavor, labels=json.dumps(labels),modelURI=modelURI,
                              input_signature=json.dumps(input_fields), output_signature=output_signature,
                              classification_type=classification_type)
                aimodel.save()
            if source_type=='file':
                #save the file
                 # Define the file path where the file will be saved
                model_file = request.POST.get('file')
                filepath = os.path.join(settings.MEDIA_ROOT, model_file.name)
                # Save the file
                with default_storage.open(filepath, 'wb+') as destination:
                    for chunk in model_file.chunks():
                        destination.write(chunk)
                code_s="model=load_model(\""+filepath+"\")"
                flavorsFactory = FlavorsFactory()
                modelURI = flavorsFactory.upload_model(flavor, name, code_s, input_signature, output_signature)
                aimodel = AIModel(name=name, flavor=flavor, labels=json.dumps(labels),modelURI=modelURI,
                              input_signature=json.dumps(input_fields), output_signature=output_signature,
                              classification_type=classification_type)
                aimodel.save()
            return Response(status=status.HTTP_200_OK)


    else:
        form = AIModelForm()
        input_formset = InputFieldFormSet(prefix='input')
        output_formset = OutputFieldFormSet(prefix='output')

    context = {
        'form': form,
        'input_formset': input_formset,
        'output_formset': output_formset,
    }

    return render(request, 'upload_model2.html', context)

# monetor model (draw charts predecton rating with time, show reviews on the explainations and on the model)

def plot_feedback_ratings_over_time(model_id):
    model_instance = get_object_or_404(AIModel, id=model_id)
    queries = Query.objects.filter(model=model_instance)
    
    times = []
    feedback_ratings = []
    feedback_details = []  # To store detailed feedback data

    for query in queries:
        try:
            feedback = Feedback.objects.get(query=query)
            # Extracting the star ratings and calculating the average rating
            star_ratings = feedback.star_ratings
            ratings = list(star_ratings.values())
            average_rating = sum(ratings) / len(ratings)
            feedback_ratings.append(average_rating)
            times.append(query.created_at)
            
            # Store detailed feedback
            feedback_details.append({
                'created_at': query.created_at,
                'average_rating': average_rating,
                'star_ratings': star_ratings,
                'text_feedback': feedback.text_feedback
            })
        except Feedback.DoesNotExist:
            continue

    if times and feedback_ratings:
        times, feedback_ratings = zip(*sorted(zip(times, feedback_ratings)))

        # Plotting the feedback ratings over time
        plt.figure(figsize=(10, 6))
        plt.plot(times, feedback_ratings, marker='o', linestyle='-', color='b')
        plt.xlabel('Time')
        plt.ylabel('Average Feedback Rating')
        plt.title('Feedback Ratings Over Time')
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.tight_layout()

        # Save the plot to a PNG image in memory and encode it in base64
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
        buf.close()

        return image_base64#, feedback_details
    else:
        return None, []



from collections import defaultdict
from django.shortcuts import render, get_object_or_404
from .models import AIModel, Query, Feedback, Explanation

def model_feedback_view(request, model_id):
    model_instance = get_object_or_404(AIModel, id=model_id)
    queries = Query.objects.filter(model=model_instance)
    
    feedback_details = []
    
    for query in queries:
        try:
            feedback = Feedback.objects.get(query=query)
            ratings = list(feedback.star_ratings.values())
            average_rating = sum(ratings) / len(ratings)
            
            # Gather explanations and calculate average ratings for each explainer type
            explanations = Explanation.objects.filter(query=query)
            explainer_ratings = defaultdict(list)
            
            for explanation in explanations:
                explainer_ratings[explanation.explainaing_algo].append(explanation.rating)
            
            explainer_avg_ratings = {explainer: sum(ratings) / len(ratings) for explainer, ratings in explainer_ratings.items()}
            
            feedback_details.append({
                'created_at': feedback.created_at,
                'average_rating': average_rating,
                'text_feedback': feedback.text_feedback,
                'star_ratings': feedback.star_ratings,
                'explainer_avg_ratings': explainer_avg_ratings
            })
        except Feedback.DoesNotExist:
            continue
    
    context = {
        'image_base64': plot_feedback_ratings_over_time(model_id),
        'model': model_instance,
        'feedback_details': feedback_details
    }

    return render(request, 'model_feedback.html', context)
