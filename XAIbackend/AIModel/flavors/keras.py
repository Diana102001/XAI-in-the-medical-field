from .flavor import flavor
import mlflow
import numpy as np
class Keras(flavor):
    codeFilePath = "playground/flavors/kerasCode.py"  # Class-level constant

    def __init__(self):
        super().__init__(self.codeFilePath)

    def runCode(self,name,model,inputSchema,outputSchema):
        with open(self.codeFilePath, "r") as file:
            full = file.read()
            
    
        input_position = full.find('# input_schema')
        full=full[:input_position] + inputSchema + full[input_position:]
        output_position = full.find('# output_schema')
        full=full[:output_position] + outputSchema + full[output_position:]
        name_position = full.find('# name')
        full=full[:name_position] + '"'+ name +'"' + full[name_position:]
        model_position = full.find('# Insert your snippet here')
        full=full[:model_position] + model + full[model_position:]
        print(full)

        exec_env = {}
        print("exe env",exec_env)
        exec(full, exec_env)
        uri=exec_env.get('model_uri')
        return uri


    def useModel(self,input_data,modelURI):
        # image=input_data['input_image']
        loaded_model = mlflow.keras.load_model(modelURI)
        result=loaded_model(input_data)
        return result

