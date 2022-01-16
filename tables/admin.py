from django.contrib import admin
from tables.models import organisationTable, measurementUnitTable, statusTable, rawMaterialsTable, equipmentTable, \
    subcomponentsTable


@admin.register(organisationTable, measurementUnitTable, statusTable, rawMaterialsTable, equipmentTable,
                subcomponentsTable)
class excelFileAdmin(admin.ModelAdmin):
    pass
