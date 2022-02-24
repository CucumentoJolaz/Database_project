from django import forms

from tables.forms.abstract_forms import equipmentTableForm, subcomponentsTableForm, rawMaterialsTableForm, \
    statusTableForm, \
    organisationTableForm, measurementUnitTableForm, documentTableForm, departmentTableForm, documentTypeTableForm


# introdusing new styles for demonstration forms

class demonstrationInitForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(forms.ModelForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'demoTableForm', 'disabled': ""})
        self.fields['description'].widget.attrs.update({'class': 'demoTableForm descriptionInput',
                                                        'disabled': ""})


class equipmentTableFormDemo(demonstrationInitForm, equipmentTableForm):
    pass


class subcomponentsTableFormDemo(demonstrationInitForm, subcomponentsTableForm):
    pass


class rawMaterialsTableFormDemo(demonstrationInitForm, rawMaterialsTableForm):
    pass


class statusTableFormDemo(demonstrationInitForm, statusTableForm):
    pass


class organisationTableFormDemo(demonstrationInitForm, organisationTableForm):
    pass


class measurementUnitTableFormDemo(demonstrationInitForm, measurementUnitTableForm):
    pass


class documentTableFormDemo(demonstrationInitForm, documentTableForm):
    pass


class departmentTableFormDemo(demonstrationInitForm, departmentTableForm):
    pass


class documentTypeTableFormDemo(demonstrationInitForm, documentTypeTableForm):
    pass
