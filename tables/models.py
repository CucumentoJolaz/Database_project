from django.db import models
from general.models import abstractFolder, excelFolder
from django.contrib.auth.models import User


class organisationTable(abstractFolder):
    address = models.CharField(max_length=500)
    parentFolder = models.ForeignKey(excelFolder, on_delete=models.SET_NULL, blank=True, null=True)


class measurementUnitTable(abstractFolder):
    parentFolder = models.ForeignKey(excelFolder, on_delete=models.SET_NULL, blank=True, null=True)


class statusTable(abstractFolder):
    parentFolder = models.ForeignKey(excelFolder, on_delete=models.SET_NULL, blank=True, null=True)

    @classmethod
    def getDefaultPk(cls):
        status, created = cls.objects.get_or_create(title='В работе')
        return status.pk


class departmentTable(abstractFolder):
    parentFolder = models.ForeignKey(excelFolder, on_delete=models.SET_NULL, blank=True, null=True)


class documentTypeTable(abstractFolder):
    parentFolder = models.ForeignKey(excelFolder, on_delete=models.SET_NULL, blank=True, null=True)


class documentTable(abstractFolder):
    coAuthor = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='coAuthor')
    reviewer = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='reviewer')
    documentType = models.ForeignKey(documentTypeTable, on_delete=models.SET_NULL, blank=True, null=True)
    checkUntil = models.DateTimeField(blank=True, null=True)
    approveUntil = models.DateTimeField(blank=True, null=True)
    department = models.ForeignKey(departmentTable, on_delete=models.SET_NULL, blank=True, null=True)
    parentFolder = models.ForeignKey(excelFolder, on_delete=models.SET_NULL, blank=True, null=True)


class equipmentTable(abstractFolder):
    productivity = models.FloatField(default=0)  # kg/hour
    exploitationCost = models.FloatField(default=0)  # thousand rub/hour
    serialNumber = models.CharField(default="", max_length=300)
    organisation = models.ForeignKey(organisationTable, on_delete=models.SET_NULL, null=True, blank=True)
    parentFolder = models.ForeignKey(excelFolder, on_delete=models.SET_NULL, blank=True, null=True)
    department = models.ForeignKey(departmentTable, on_delete=models.SET_NULL, blank=True, null=True)


class rawMaterialsTable(abstractFolder):
    originalAmount = models.FloatField(default=0)
    availableAmount = models.FloatField(default=0)
    cost = models.FloatField(default=0)
    serialNumber = models.CharField(default="", max_length=300)
    organisation = models.ForeignKey(organisationTable, on_delete=models.SET_NULL, null=True, blank=True)
    measurementUnit = models.ForeignKey(measurementUnitTable, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.ForeignKey(statusTable, on_delete=models.SET_DEFAULT, default=statusTable.getDefaultPk)
    parentFolder = models.ForeignKey(excelFolder, on_delete=models.SET_NULL, blank=True, null=True)
    department = models.ForeignKey(departmentTable, on_delete=models.SET_NULL, blank=True, null=True)


class subcomponentsTable(abstractFolder):
    status = models.ForeignKey(statusTable, on_delete=models.SET_DEFAULT, default=statusTable.getDefaultPk)
    originalAmount = models.FloatField(default=0)
    creationTime = models.TimeField(blank=True, null=True)
    availableAmount = models.FloatField(default=0)
    cost = models.FloatField(default=0)
    parentFolder = models.ForeignKey(excelFolder, on_delete=models.SET_NULL, blank=True, null=True)
    department = models.ForeignKey(departmentTable, on_delete=models.SET_NULL, blank=True, null=True)
