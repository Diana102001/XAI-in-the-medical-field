from .LimeImage import LimeImage
from .LimeTabular import LimeTabular

class ExplainerFactory:
    def create_explainers(self, explainer_type):
        explainers = []
        
        if explainer_type == 'image':
            explainers.append(LimeImage())
            # explainers.append(ShapImage())
        elif explainer_type == 'tabular':
            explainers.append(LimeTabular())
            # explainers.append(ShapTabular())
        else:
            raise ValueError("Unknown explainer type")

        return explainers
