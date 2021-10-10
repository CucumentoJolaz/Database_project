from django.db import models
from general.models import abstractFolder, excelFolder
# Create your models here.


class rawMaterialsTable(abstractFolder):
    status = models.CharField(default = "", max_length = 200)
    originalAmount = models.FloatField(default = 0)
    units = models.CharField(default = "", max_length = 300)
    availableAmount = models.FloatField(default = 0)
    cost = models.FloatField(default = 0)
    serialNumber = models.CharField(default = "", max_length = 300)
    provider = models.CharField(default = "", max_length = 300)
    parentFolder = models.ForeignKey(excelFolder, on_delete=models.SET_NULL, default=2, null = True)


class equipmentTable(abstractFolder):
    productivity = models.FloatField(default = 0) # kg/hour
    exploitationCost = models.FloatField(default = 0) # thousand rub/hour
    serialNumber = models.CharField(default = "", max_length = 300)
    provider = models.CharField(default = "", max_length = 300)
    parentFolder = models.ForeignKey(excelFolder, on_delete=models.SET_NULL, default=2, null = True)

class subcomponentsTable(abstractFolder):
    status = models.CharField(default="", max_length=200)
    originalAmount = models.FloatField(default=0)
    creationTime = models.TimeField()
    availableAmount = models.FloatField(default=0)
    cost = models.FloatField(default=0)
    parentFolder = models.ForeignKey(excelFolder, on_delete=models.SET_NULL, default=2, null = True)
