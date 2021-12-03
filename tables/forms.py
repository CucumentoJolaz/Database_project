from general.forms import excelFolderForm
from tables.models import subcomponentsTable, rawMaterialsTable, equipmentTable, organisationTable, \
    measurementUnitTable, statusTable
from django import forms


class organisationChoice(forms.ModelChoiceField):

    def label_from_instance(self, organisationObj):
        return f'{organisationObj.title}'

class statusChoice(forms.ModelChoiceField):

    def label_from_instance(self, statusObj):
        return f'{statusObj.title}'

# creating 3 different kind of forms, which supposed to display a form to
# create an instanse of it's model
# inheritance from excelFolderForm was made to inherit save() function
class subcomponentsTableForm(excelFolderForm):
    class Meta:
        model = subcomponentsTable
        fields = ('title',
                  'status', 'originalAmount', 'availableAmount',
                  'creationTime', 'cost', 'path')

        widgets = {
            'path': forms.HiddenInput(), }


class rawMaterialsTableForm(excelFolderForm):
    class Meta:
        model = rawMaterialsTable
        fields = ['title',
                  'status', 'originalAmount', 'availableAmount',
                  'cost',
                  'units', 'serialNumber',
                  'organisation', 'path']
        widgets = {
            'path': forms.HiddenInput(), }

    organisation = organisationChoice(
        queryset=organisationTable.objects.filter(deleted=False)
    )

    status = organisationChoice(
        queryset=statusTable.objects.filter(deleted=False)
    )

class equipmentTableForm(excelFolderForm):
    class Meta:
        model = equipmentTable
        fields = ('title',
                  'productivity', 'exploitationCost',
                  'serialNumber',
                  'organisation', 'path')
        widgets = {
            'path': forms.HiddenInput(),
        }

    organisation = organisationChoice(
        queryset=organisationTable.objects.filter(deleted=False)
    )


class measurementUnitTableForm(excelFolderForm):
    class Meta:
        model = measurementUnitTable
        fields = ('title',
                  'description', 'path')
        widgets = {
            'path': forms.HiddenInput(),
        }


class statusTableForm(excelFolderForm):
    class Meta:
        model = statusTable
        fields = ('title',
                  'description', 'path')
        widgets = {
            'path': forms.HiddenInput(),
        }


class organisationTableForm(excelFolderForm):
    class Meta:
        model = organisationTable
        fields = ('title',
                  'description', 'path',
                  'address')
        widgets = {
            'path': forms.HiddenInput(),
        }


# creating 3 different kind of forms, which supposed to display a form to
# UPDATE an instanse of it's model
# inheritance from excelFolderForm was made to inherit all fields of CREATION forms
# but to change save() method
class equipmentTableFormUpdate(equipmentTableForm):
    def save(self, commit=True):
        instance = super(forms.ModelForm, self).save(commit=False)  # inherit as original save() from vanila forms
        if commit:
            instance.save()
        return instance


class subcomponentsTableFormUpdate(subcomponentsTableForm):
    def save(self, commit=True):
        instance = super(forms.ModelForm, self).save(commit=False)
        if commit:
            instance.save()
        return instance


class rawMaterialsTableFormUpdate(rawMaterialsTableForm):
    def save(self, commit=True):
        instance = super(forms.ModelForm, self).save(commit=False)
        if commit:
            instance.save()
        return instance


class statusTableFormUpdate(statusTableForm):
    def save(self, commit=True):
        instance = super(forms.ModelForm, self).save(commit=False)
        if commit:
            instance.save()
        return instance


class organisationTableFormUpdate(organisationTableForm):
    def save(self, commit=True):
        instance = super(forms.ModelForm, self).save(commit=False)
        if commit:
            instance.save()
        return instance


class measurementUnitTableFormUpdate(measurementUnitTableForm):
    def save(self, commit=True):
        instance = super(forms.ModelForm, self).save(commit=False)
        if commit:
            instance.save()
        return instance