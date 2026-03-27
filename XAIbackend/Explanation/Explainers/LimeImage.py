from lime import lime_image
from skimage.segmentation import mark_boundaries
import matplotlib.pyplot as plt
import numpy as np
import cv2
from .ImageExplianer import ImageExplainer


class LimeImage(ImageExplainer):
    def __init__(self):
        self.name="Lime Image"
        
    def explaine(self,model,test_image_dict):
        test_image=list(test_image_dict.values())[0]
        explainer = lime_image.LimeImageExplainer()
        # Explain prediction
        explanation=explainer.explain_instance(test_image, model.predict, top_labels=5, hide_color=0, num_samples=1000)
        # Show explanation
        temp, mask = explanation.get_image_and_mask(explanation.top_labels[0], positive_only=True, num_features=5, hide_rest=False)
        overlay_image = mark_boundaries(temp, mask)
        # Convert image from float64 to uint8 (required for OpenCV)
        overlay_image = (overlay_image * 255).astype(np.uint8)
        # Save the image as JPEG using OpenCV
        path='overlay_image.jpg'
        cv2.imwrite(path, cv2.cvtColor(overlay_image, cv2.COLOR_RGB2BGR))
        return path

