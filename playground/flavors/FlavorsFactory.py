import mlflow

from playground.ModelSingelton import AIModelSingleton
from .pytorch import pytorch
from .keras import Keras
class FlavorsFactory:

    def getModel(self,aimodel):
        # uri=aimodel.modelURI
        # flavor=aimodel.flavor
        # flavor_module = getattr(mlflow, flavor)
        # loaded_model_method = getattr(flavor_module, 'load_model')
        m=AIModelSingleton.get_model(model_id=aimodel.id)
        return m

    def useModel(self, model, input_data):
        # model_flavor=model.flavor
        # flavor_module = getattr(mlflow, model_flavor)
        # loaded_model_method = getattr(flavor_module, 'load_model')
        m=AIModelSingleton.get_model(model_id=model.id)
        output_data=m(input_data)
        return output_data
               
        # mlflow.<model_flavor>.log_model()
    def upload_model(self,flavor,name,model,inputSchema,outputSchema):
        if flavor=='pytorch':
            f=pytorch()
            return f.runCode(name,model,inputSchema,outputSchema)
        elif flavor=='keras':
            f=Keras()
            return f.runCode(name,model,inputSchema,outputSchema)

            
    

