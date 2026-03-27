from abc import ABC, abstractmethod
from .Explainer import Explainer
from lime import lime_image

class TabularExplainer(Explainer):
    @abstractmethod
    def explaine(self,model,data,instance):
        pass