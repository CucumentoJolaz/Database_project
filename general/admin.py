from django.contrib import admin
from general.models import excelFile, excelFolder


@admin.register(excelFile, excelFolder)
class excelFileAdmin(admin.ModelAdmin):
    pass

# @admin.register(excelFolder)
# class excelFileAdmin(admin.ModelAdmin):
#     pass
