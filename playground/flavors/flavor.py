from abc import ABC, abstractmethod

class flavor(ABC):
    def __init__(self,codeFilePath):
        self.codeFilePath=codeFilePath
        
    @abstractmethod
    def runCode(self,codeFilePath,name,model,inputSchema,outputSchema):
        pass

    @abstractmethod
    def useModel(self,input_data,modelURI):
        pass
