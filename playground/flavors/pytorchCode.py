import mlflow
from torchsummary import summary
import torchvision.models as models
from mlflow.models import ModelSignature
from mlflow.types.schema import Schema, ColSpec
import tensorflow as tf
from mlflow.types import TensorSpec
import numpy as np

mlflow.set_tracking_uri("http://127.0.0.1:5000")


input_schema= # input_schema
output_schema= # output_schema
signature = ModelSignature(inputs=input_schema, outputs=output_schema)

with mlflow.start_run() as run:
    # Insert your snippet here
    name=# name
    m=mlflow.pytorch.log_model(model,name,signature=signature)
    model_uri = m.model_uri
    print(model_uri)