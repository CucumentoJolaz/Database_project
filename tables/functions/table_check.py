from dataclasses import dataclass

from tables.forms.demonstration_forms import equipmentTableFormDemo, departmentTableFormDemo, documentTypeTableFormDemo, \
    documentTableFormDemo, measurementUnitTableFormDemo, statusTableFormDemo, organisationTableFormDemo, \
    subcomponentsTableFormDemo, rawMaterialsTableFormDemo
from tables.models import equipmentTable, subcomponentsTable, rawMaterialsTable, organisationTable, statusTable, \
    measurementUnitTable, documentTable, documentTypeTable, departmentTable
from tables.forms.creation_forms import subcomponentsTableFormCreate, rawMaterialsTableFormCreate, \
    equipmentTableFormCreate, measurementUnitTableFormCreate,\
    statusTableFormCreate, organisationTableFormCreate, departmentTableFormCreate, \
    documentTypeTableFormCreate, documentTableFormCreate
from tables.forms.update_forms import equipmentTableFormUpdate, subcomponentsTableFormUpdate, \
    rawMaterialsTableFormUpdate, \
    statusTableFormUpdate, organisationTableFormUpdate, measurementUnitTableFormUpdate, documentTableFormUpdate, \
    documentTypeTableFormUpdate, departmentTableFormUpdate


@dataclass
class tableInfo():
    dbTitle: str
    model: object
    createForm: object
    updateForm: object
    demoForm: object


class tableInfoProcessor():
    tableList = [
        tableInfo(dbTitle="equipment",
                  model=equipmentTable,
                  createForm=equipmentTableFormCreate,
                  updateForm=equipmentTableFormUpdate,
                  demoForm=equipmentTableFormDemo),
        tableInfo(dbTitle="rawMaterial",
                  model=rawMaterialsTable,
                  createForm=rawMaterialsTableFormCreate,
                  updateForm=rawMaterialsTableFormUpdate,
                  demoForm=rawMaterialsTableFormDemo),
        tableInfo(dbTitle="subcomponent",
                  model=subcomponentsTable,
                  createForm=subcomponentsTableFormCreate,
                  updateForm=subcomponentsTableFormUpdate,
                  demoForm=subcomponentsTableFormDemo),
        tableInfo(dbTitle="organisation",
                  model=organisationTable,
                  createForm=organisationTableFormCreate,
                  updateForm=organisationTableFormUpdate,
                  demoForm=organisationTableFormDemo),
        tableInfo(dbTitle="status",
                  model=statusTable,
                  createForm=statusTableFormCreate,
                  updateForm=statusTableFormUpdate,
                  demoForm=statusTableFormDemo),
        tableInfo(dbTitle="measurementUnit",
                  model=measurementUnitTable,
                  createForm=measurementUnitTableFormCreate,
                  updateForm=measurementUnitTableFormUpdate,
                  demoForm=measurementUnitTableFormDemo),
        tableInfo(dbTitle="document",
                  model=documentTable,
                  createForm=documentTableFormCreate,
                  updateForm=documentTableFormUpdate,
                  demoForm=documentTableFormDemo),
        tableInfo(dbTitle="documentType",
                  model=documentTypeTable,
                  createForm=documentTypeTableFormCreate,
                  updateForm=documentTypeTableFormUpdate,
                  demoForm=documentTypeTableFormDemo),
        tableInfo(dbTitle="department",
                  model=departmentTable,
                  createForm=departmentTableFormCreate,
                  updateForm=departmentTableFormUpdate,
                  demoForm=departmentTableFormDemo)
    ]

    def tableTypeModel(self, tableName: str):
        """
        Accepting string which specifies table type, and returning model type
        tableTypeModel(self, tableName: str):
        """
        for tableInfo in self.tableList:
            if tableName == tableInfo.dbTitle:
                return tableInfo.model

    def tableTypeFormCreate(self, tableName: str):
        """
        Accepting string which specifies table type, and returning form type
        tableTypeFormCreate(self, tableName: str)
        """
        for tableInfo in self.tableList:
            if tableName == tableInfo.dbTitle:
                return tableInfo.createForm

    def tableTypeFormUpdate(self, tableName: str):
        """
        Accepting string which specifies table type, and returning form Update type
        tableTypeFormUpdate(self, tableName: str)
        """
        for tableInfo in self.tableList:
            if tableName == tableInfo.dbTitle:
                return tableInfo.updateForm

    def tableTypeFormDemo(self, tableName: str):
        """
        Accepting string which specifies table type, and returning form  Demo type
        tableTypeFormUpdate(self, tableName: str)
        """
        for tableInfo in self.tableList:
            if tableName == tableInfo.dbTitle:
                return tableInfo.demoForm

    def tableTypeText(self, tableModel):
        """
        Accepting table model and returning string which represents it
        tableTypeText(self, tableModel)
        """
        for tableInfo in self.tableList:
            if isinstance(tableInfo.model, tableModel):
                return tableInfo.dbTitle

    def getTables(self, theFolderObject):
        """
        Receiving primal folder instance, and returning all of it's tables instances, which lies within
        getTables(self, theFolderObject):
        """
        if theFolderObject.tableName:
            for tableInfo in self.tableList:
                if theFolderObject.tableName == tableInfo.dbTitle:
                    return tableInfo.model.objects.filter(parentFolder__pk=theFolderObject.pk)
