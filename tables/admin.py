from django.contrib import admin
from tables.models import organisationTable, measurementUnitTable, statusTable, rawMaterialsTable, equipmentTable, \
    subcomponentsTable, documentTable, documentTypeTable, departmentTable


@admin.register(organisationTable, measurementUnitTable, statusTable, rawMaterialsTable, equipmentTable,
                subcomponentsTable, documentTable, documentTypeTable, departmentTable)
class excelFileAdmin(admin.ModelAdmin):
    pass
