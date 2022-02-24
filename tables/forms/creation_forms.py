from django import forms

from tables.forms.abstract_forms import subcomponentsTableForm, rawMaterialsTableForm, equipmentTableForm, \
    measurementUnitTableForm, statusTableForm, organisationTableForm, documentTableForm, departmentTableForm, \
    documentTypeTableForm
from general.forms import abstractFolderForm

defaultChoiceList = 'Не указана'


# creating N different kind of forms, which supposed to display a form to
# create an instance of it's model
# inheritance from abstractFolderForm was made to inherit save() function


class somethingChoice(forms.ModelChoiceField):

    def label_from_instance(self, somethingObj):
        if "title" in somethingObj.__dict__:
            return f'{somethingObj.title}'
        elif "nickname" in somethingObj.__dict__:
            return f'{somethingObj.nickname}'


class subcomponentsTableFormCreate(abstractFolderForm, subcomponentsTableForm):
    pass

class rawMaterialsTableFormCreate(abstractFolderForm, rawMaterialsTableForm):
    pass


class equipmentTableFormCreate(abstractFolderForm, equipmentTableForm):
    pass


class measurementUnitTableFormCreate(abstractFolderForm, measurementUnitTableForm):
    pass


class statusTableFormCreate(abstractFolderForm, statusTableForm):
    pass


class organisationTableFormCreate(abstractFolderForm, organisationTableForm):
    pass


class documentTableFormCreate(abstractFolderForm, documentTableForm):
    pass


class departmentTableFormCreate(abstractFolderForm, departmentTableForm):
    pass


class documentTypeTableFormCreate(abstractFolderForm, documentTypeTableForm):
    pass
