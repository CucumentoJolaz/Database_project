from dataclasses import dataclass

from tables.models import equipmentTable, subcomponentsTable, rawMaterialsTable, organisationTable, statusTable, measurementUnitTable
from tables.forms import equipmentTableForm, subcomponentsTableForm, rawMaterialsTableForm, organisationTableForm, \
    statusTableForm, measurementUnitTableForm, organisationTableFormUpdate, statusTableFormUpdate, \
    measurementUnitTableFormUpdate
from tables.forms import equipmentTableFormUpdate, subcomponentsTableFormUpdate, rawMaterialsTableFormUpdate


@dataclass
class tableInfo():
    dbTitle: str
    model: object
    form: object
    updateForm: object


class tableInfoProcessor():
    tableList = [
        tableInfo(dbTitle="equipment", model=equipmentTable, form=equipmentTableForm, updateForm=equipmentTableFormUpdate),
        tableInfo(dbTitle="rawMaterial", model=rawMaterialsTable, form=rawMaterialsTableForm, updateForm=rawMaterialsTableFormUpdate),
        tableInfo(dbTitle="subcomponent", model=subcomponentsTable, form=subcomponentsTableForm, updateForm=subcomponentsTableFormUpdate),
        tableInfo(dbTitle="organisation", model=organisationTable, form=organisationTableForm, updateForm=organisationTableFormUpdate),
        tableInfo(dbTitle="status", model=statusTable, form=statusTableForm, updateForm=statusTableFormUpdate),
        tableInfo(dbTitle="measurementUnit", model=measurementUnitTable, form=measurementUnitTableForm, updateForm=measurementUnitTableFormUpdate),
    ]

    def tableTypeModel(self, tableName: str):
        """accepting string which specifies table type, and returning model type"""
        for tableInfo in self.tableList:
            if tableName == tableInfo.dbTitle:
                return tableInfo.model

    def tableTypeForm(self, tableName: str):
        """accepting string which specifies table type, and returning form type"""
        for tableInfo in self.tableList:
            if tableName == tableInfo.dbTitle:
                return tableInfo.form

    def tableTypeFormUpdate(self, tableName: str):
        """accepting string which specifies table type, and returning form type"""
        for tableInfo in self.tableList:
            if tableName == tableInfo.dbTitle:
                return tableInfo.updateForm

    def tableTypeText(self, tableModel):
        """Accepting table model and returning string which represents it"""
        for tableInfo in self.tableList:
            if isinstance(tableInfo.model, tableModel):
                return tableInfo.dbTitle

    def getTables(self, theFolderObject):
        """Receiving primal folder instance, and returning all of it's tables instances, which lies within"""
        if theFolderObject.tableName:
            for tableInfo in self.tableList:
                if theFolderObject.tableName == tableInfo.dbTitle:
                    return tableInfo.model.objects.filter(parentFolder__pk=theFolderObject.pk)
