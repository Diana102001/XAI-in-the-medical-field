from abc import ABC, abstractmethod

class Explainer(ABC):
    def init(self,name):
        self.name=name