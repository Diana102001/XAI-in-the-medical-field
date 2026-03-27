from django.db import models

# Create your models here.
class AIModel(models.Model):
    class ClassificationType(models.TextChoices):
        BINARY = 'binary', 'Binary'
        MULTI_CLASSES = 'multi_classes', 'Multi Classes'
        MULTI_LABELS = 'multi_labels', 'Multi Labels'

    modelURI = models.CharField(max_length=200, unique=True, null=False)
    name = models.CharField(max_length=100)#
    flavor = models.CharField(max_length=100)#
    labels = models.JSONField()#
    input_signature = models.JSONField()#
    output_signature = models.JSONField()#
    classification_type = models.CharField(
        max_length=20,
        choices=ClassificationType.choices,
        default=ClassificationType.BINARY
    )#
    dataset_path=models.CharField(max_length=200,null=True)
    
    def __str__(self):
        return self.name