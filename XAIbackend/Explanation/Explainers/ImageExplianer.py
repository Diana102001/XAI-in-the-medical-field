from abc import ABC, abstractmethod
from .Explainer import Explainer
from lime import lime_image

class ImageExplainer(Explainer):
    @abstractmethod
    def explaine(self,model,test_image):
        pass

    def describeImageExplanation(self,image):
        enhanced_explanation="The image is a chest X-ray, and the yellow lines highlight the regions of the image that were most important in the AI model's decision to classify it as \"normal\" (not COVID-19)\nHere's a breakdown of what the yellow lines might indicate:\nLung Fields: The lines around the lungs suggest the model focused on the overall appearance of the lung tissue. A healthy lung pattern would show clear, well-defined air spaces, without any signs of opacities (white spots) or infiltrates (fluid buildup) that could be associated with COVID-19.\nHeart Shadow: The line around the heart area could indicate that the model observed a normal heart size and shape, which is another factor that can be affected by COVID-19.\nClavicle: The line around the clavicle (collarbone) may be less significant in the classification, but it could show that the model noticed the absence of any bone abnormalities or fractures, which could sometimes be a sign of severe illness."
        return enhanced_explanation