from typing import Any
from django.db import models
import numpy as np
from django.contrib.auth.models import User
import json
import cv2
import os
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator




# Create your models here.
class AIModel(models.Model):
    class ClassificationType(models.TextChoices):
        BINARY = 'binary', 'Binary'
        MULTI_CLASSES = 'multi_classes', 'Multi Classes'
        MULTI_LABELS = 'multi_labels', 'Multi Labels'

    modelURI = models.CharField(max_length=200, unique=True, null=False)
    name = models.CharField(max_length=100)#
    flavor = models.CharField(max_length=100)#
    labels = models.JSONField()#
    input_signature = models.JSONField()#
    output_signature = models.JSONField()#
    classification_type = models.CharField(
        max_length=20,
        choices=ClassificationType.choices,
        default=ClassificationType.BINARY
    )#
    dataset_path=models.CharField(max_length=200,null=True)

class Query(models.Model):
  user=models.ForeignKey(User,on_delete=models.CASCADE)
  model=models.ForeignKey(AIModel,on_delete=models.CASCADE)
  query_input=models.JSONField()
  query_output=models.JSONField()
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  def save(self, *args, **kwargs):
        if not self.pk:  
           print("already here  :)")
        super().save(*args, **kwargs)

  def get_input_and_input_type(self):
  
      input_type = "tabular"
      input_data=json.loads(self.query_input)
      print(input_data)    
      for key, value in input_data.items():
            if isinstance(value, str):
                if os.path.isfile(value) and (value.lower().endswith('.png') or value.lower().endswith('.jpg') or value.lower().endswith('.jpeg')):
                    image = cv2.imread(value)
                    input_data[key] = image
                    input_type = "image"
      return input_data,input_type



class Feedback(models.Model):
  query=models.OneToOneField(Query,on_delete=models.CASCADE)
  star_ratings=models.JSONField()
  text_feedback=models.TextField()
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  def get_rating_questions():
        return [
            "How well did the prediction meet your expectations?",
            "How much clearer did the explanations make the prediction?",
            "How confident are you in the prediction after reviewing the explanations?"
        ]

def validate_half_rating(value):
    if value % 0.25 != 0:
        raise ValidationError('Rating must be in increments of 0.5.')

class Explanation(models.Model):
  query=models.ForeignKey(Query,on_delete=models.CASCADE)
  explainaing_algo=models.CharField(max_length=100)
  explanation_type=models.CharField(max_length=100)
  explain_input=models.JSONField()
  explain_output=models.JSONField()
  created_at = models.DateTimeField(auto_now_add=True)
  rating=models.FloatField(default=0, validators=[
        MinValueValidator(0),
        MaxValueValidator(5.0),
        validate_half_rating
    ])

  def save(self, *args, **kwargs):
        if not self.pk:  
           print("already here  :)")
        super().save(*args, **kwargs)

class Chat(models.Model):
  query=models.ForeignKey(Query,on_delete=models.CASCADE)
  user=models.ForeignKey(User,on_delete=models.CASCADE)
  sent_message = models.JSONField()
  received_message=models.JSONField()
  created_at = models.DateTimeField(auto_now_add=True)
