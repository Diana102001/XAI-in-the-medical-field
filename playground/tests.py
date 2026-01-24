from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from .models import AIModel
from .serializers import AIModelSerializer



from django.test import TestCase, Client
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django import forms
from .models import AIModel
from .forms import AIModelForm, InputFieldFormSet, OutputFieldFormSet
from unittest.mock import patch
import json

class UploadModelTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.url = reverse('upload_model')  # Replace with the correct URL name for your upload_model view

    @patch('playground.views.GetSignature')
    @patch('playground.views.FlavorsFactory')
    def test_upload_model_valid(self, MockFlavorsFactory, MockGetSignature):
        MockGetSignature.return_value = 'input_signature'
        mock_flavors_factory = MockFlavorsFactory.return_value
        mock_flavors_factory.upload_model.return_value = 'modelURI'

        post_data = {
            'classification_type': 'binary',
            'flavor': 'flavor1',
            'name': 'Model 1',
            'num_labels': 2,
            'min_labels': 1,
            'max_labels': 3,
            'label_0': 'label1',
            'label_1': 'label2',
            'source_type': 'code',
            'code_snippet': 'some_code_here'
        }
        input_data = {
            'input_field_0': 'input_data_0',
            'input_field_1': 'input_data_1'
        }
        output_data = {
            'output_field_0': 'output_data_0',
            'output_field_1': 'output_data_1'
        }

        # Simulate POST request
        response = self.client.post(self.url, {**post_data, **input_data, **output_data})

        # Verify the response
        self.assertEqual(response.status_code, 302)  # Redirect status code

        # Verify that an AIModel instance was created
        aimodel = AIModel.objects.first()
        self.assertIsNotNone(aimodel)
        self.assertEqual(aimodel.name, 'Model 1')
        self.assertEqual(aimodel.flavor, 'flavor1')
        self.assertEqual(json.loads(aimodel.labels), {
            'num_labels': 2,
            'label_names': ['label1', 'label2'],
            'min_labels': 1,
            'max_labels': 3
        })
        self.assertEqual(aimodel.input_signature, json.dumps([
            {'input_field_0': 'input_data_0'},
            {'input_field_1': 'input_data_1'}
        ]))
        self.assertEqual(aimodel.output_signature, 'Schema([TensorSpec(np.dtype("float32"),(-1,2), "class"),])')

    @patch('playground.views.GetSignature')
    def test_upload_model_invalid(self, MockGetSignature):
        MockGetSignature.return_value = 'input_signature'
        
        # Simulate POST request with missing required fields
        response = self.client.post(self.url, {})

        # Verify the response
        self.assertEqual(response.status_code, 200)  # Should re-render the form with errors
        self.assertContains(response, 'This field is required.')  # Check for form errors

    def test_upload_model_with_files(self):
        # Simulate a POST request with a file upload (if applicable)
        post_data = {
            'classification_type': 'binary',
            'flavor': 'flavor1',
            'name': 'Model 1',
            'num_labels': 2,
            'min_labels': 1,
            'max_labels': 3,
            'label_0': 'label1',
            'label_1': 'label2',
            'source_type': 'file',
        }
        files = {
            'model_file': SimpleUploadedFile("model.h5", b"file_content", content_type="application/x-hdf5")
        }

        response = self.client.post(self.url, post_data, FILES=files)

        # Verify the response
        # self.assertEqual(response.status_code, 302)  # Redirect status code

        # Verify that an AIModel instance was created
        aimodel = AIModel.objects.first()
        self.assertIsNotNone(aimodel)
        self.assertEqual(aimodel.name, 'Model 1')
        self.assertEqual(aimodel.flavor, 'flavor1')


from django.test import TestCase
from django import forms
from .helpers import get_field_by_type, create_dynamic_form  # Adjust the import to match your actual file structure

class TestHelpers(TestCase):

    def test_get_field_by_type_image(self):
        field = get_field_by_type('image_field', 'image')
        self.assertIsInstance(field, forms.ImageField)
        self.assertEqual(field.label, 'image_field')

    def test_get_field_by_type_float(self):
        field = get_field_by_type('float_field', 'float32')
        self.assertIsInstance(field, forms.FloatField)
        self.assertEqual(field.label, 'float_field')

    def test_get_field_by_type_int(self):
        field = get_field_by_type('int_field', 'int32')
        self.assertIsInstance(field, forms.IntegerField)
        self.assertEqual(field.label, 'int_field')

    def test_get_field_by_type_string(self):
        field = get_field_by_type('string_field', 'string')
        self.assertIsInstance(field, forms.CharField)
        self.assertEqual(field.label, 'string_field')

    def test_get_field_by_type_default(self):
        field = get_field_by_type('default_field', 'unknown_type')
        self.assertIsInstance(field, forms.CharField)
        self.assertEqual(field.label, 'default_field')

    def test_create_dynamic_form(self):
        feature_names = ['image_field', 'float_field', 'int_field', 'string_field']
        feature_types = ['image', 'float32', 'int32', 'string']
        feature_shapes = [None, None, None, None]  # Shapes are not used in get_field_by_type
        
        DynamicFormClass = create_dynamic_form(feature_names, feature_types, feature_shapes)
        form = DynamicFormClass()

        # Check that the form has the correct fields
        self.assertIn('image_field', form.fields)
        self.assertIsInstance(form.fields['image_field'], forms.ImageField)

        self.assertIn('float_field', form.fields)
        self.assertIsInstance(form.fields['float_field'], forms.FloatField)

        self.assertIn('int_field', form.fields)
        self.assertIsInstance(form.fields['int_field'], forms.IntegerField)

        self.assertIn('string_field', form.fields)
        self.assertIsInstance(form.fields['string_field'], forms.CharField)


class AIModelListTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.url = reverse('aimodels') 
        # Create some AIModel instances for testing
        self.model1 = AIModel.objects.create(
            modelURI='uri1',
            name='Model 1',
            flavor='flavor1',
            labels={"label_names": ["label1", "label2"]},
            input_signature={"input1": "float32"},
            output_signature={"output1": "float32"},
            classification_type=AIModel.ClassificationType.BINARY,
            dataset_path='/path/to/dataset1'
        )
        
        self.model2 = AIModel.objects.create(
            modelURI='uri2',
            name='Model 2',
            flavor='flavor2',
            labels={"label_names": ["label3", "label4"]},
            input_signature={"input2": "int32"},
            output_signature={"output2": "int32"},
            classification_type=AIModel.ClassificationType.MULTI_CLASSES,
            dataset_path='/path/to/dataset2'
        )
    
    def test_get_aimodel_list(self):
        # Simulate a GET request to the AIModelList view
        response = self.client.get(self.url)
        
        # Fetch models from the database and serialize them
        models = AIModel.objects.all()
        serializer = AIModelSerializer(models, many=True)
        
        # Verify the response status and content
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_get_empty_aimodel_list(self):
        # Clear the AIModel instances
        AIModel.objects.all().delete()
        
        # Simulate a GET request to the AIModelList view
        response = self.client.get(self.url)
        
        # Verify the response status and content
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])
