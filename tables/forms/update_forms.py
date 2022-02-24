from django import forms

from tables.forms.abstract_forms import equipmentTableForm, subcomponentsTableForm, rawMaterialsTableForm, \
    statusTableForm, organisationTableForm, measurementUnitTableForm, documentTableForm, departmentTableForm, \
    documentTypeTableForm


# creating different kind of forms, which supposed to display a form to
# UPDATE an instanse of it's model

class updateInitForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(forms.ModelForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'updateTableForm'})
        self.fields['description'].widget.attrs.update({'class': 'updateTableForm descriptionInput'})


class equipmentTableFormUpdate(updateInitForm, equipmentTableForm):
    pass


class subcomponentsTableFormUpdate(updateInitForm, subcomponentsTableForm):
    pass


class rawMaterialsTableFormUpdate(updateInitForm, rawMaterialsTableForm):
    pass


class statusTableFormUpdate(updateInitForm, statusTableForm):
    pass


class organisationTableFormUpdate(updateInitForm, organisationTableForm):
    pass


class measurementUnitTableFormUpdate(updateInitForm, measurementUnitTableForm):
    pass


class documentTableFormUpdate(updateInitForm, documentTableForm):
    pass


class departmentTableFormUpdate(updateInitForm, departmentTableForm):
    pass


class documentTypeTableFormUpdate(updateInitForm, documentTypeTableForm):
    pass
