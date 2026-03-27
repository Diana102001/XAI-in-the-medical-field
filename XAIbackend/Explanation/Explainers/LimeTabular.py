from lime.lime_tabular import LimeTabularExplainer
import matplotlib.pyplot as plt
import numpy as np
import cv2
from .TabularExplainer import TabularExplainer


class LimeTabular(TabularExplainer):
    def init(self):
        self.name="Lime Tabular"
    def explaine(self,model,data,class_names,instance):
        explainer = LimeTabularExplainer(data.values, class_names=class_names, discretize_continuous=True)
        # Explain the instance
        explanation = explainer.explain_instance(instance, model.predict_proba)
        return explanation

