from django.db import models
from general.models import abstractFolder, excelFolder


class organisationTable(abstractFolder):
    address = models.CharField(max_length=500)
    parentFolder = models.ForeignKey(excelFolder, on_delete=models.SET_NULL, blank=True, null=True)

class measurementUnitTable(abstractFolder):
    parentFolder = models.ForeignKey(excelFolder, on_delete=models.SET_NULL, blank=True, null=True)


class statusTable(abstractFolder):
    parentFolder = models.ForeignKey(excelFolder, on_delete=models.SET_NULL, blank=True, null=True)


class rawMaterialsTable(abstractFolder):
    originalAmount = models.FloatField(default=0)
    units = models.CharField(default="", max_length=300)
    availableAmount = models.FloatField(default=0)
    cost = models.FloatField(default=0)
    serialNumber = models.CharField(default="", max_length=300)
    organisation = models.ForeignKey(organisationTable, on_delete=models.SET_NULL, null=True, blank=True)
    measurementUnit = models.ForeignKey(measurementUnitTable, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.ForeignKey(statusTable, on_delete=models.SET_NULL, blank=True, null=True)

    parentFolder = models.ForeignKey(excelFolder, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.title


class equipmentTable(abstractFolder):
    productivity = models.FloatField(default=0)  # kg/hour
    exploitationCost = models.FloatField(default=0)  # thousand rub/hour
    serialNumber = models.CharField(default="", max_length=300)
    organisation = models.ForeignKey(organisationTable, on_delete=models.SET_NULL, null=True, blank=True)

    parentFolder = models.ForeignKey(excelFolder, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.title


class subcomponentsTable(abstractFolder):
    status = models.CharField(default="", max_length=200)
    originalAmount = models.FloatField(default=0)
    creationTime = models.TimeField()
    availableAmount = models.FloatField(default=0)
    cost = models.FloatField(default=0)

    parentFolder = models.ForeignKey(excelFolder, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.title
