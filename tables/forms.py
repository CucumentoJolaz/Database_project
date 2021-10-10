from general.forms import excelFolderForm
from tables.models import subcomponentsTable, rawMaterialsTable, equipmentTable
from django import forms

#creating 3 different kind of forms, which supposed to display a form to
#create an instanse of it's model
#inheritance from excelFolderForm was made to inherit save() function
class subcomponentsTableForm(excelFolderForm):
    class Meta:
        model = subcomponentsTable
        fields = ('title', 'path',
                  #'author',
                  'status', 'originalAmount', 'availableAmount',
                  'creationTime', 'cost')
        widgets = {
            #'author': forms.HiddenInput(),
            'path': forms.HiddenInput(),
        }


class rawMaterialsTableForm(excelFolderForm):
    class Meta:
        model = rawMaterialsTable
        fields = ('title', 'path',
                  'status', 'originalAmount', 'availableAmount',
                  'cost', #'author',
                  'units', 'serialNumber',
                  'provider')
        widgets = {
            'path': forms.HiddenInput(),
            #'author': forms.HiddenInput(),
        }


class equipmentTableForm(excelFolderForm):
    class Meta:
        model = equipmentTable
        fields = ('title', 'path',
                  'productivity', 'exploitationCost',
                  'serialNumber',
                  'provider')
        widgets = {
            'path': forms.HiddenInput(),
            # 'author': forms.HiddenInput(),
        }

#creating 3 different kind of forms, which supposed to display a form to
#UPDATE an instanse of it's model
#inheritance from excelFolderForm was made to inherit all fields of CREATION forms
#but to change save() method
class equipmentTableFormUpdate(equipmentTableForm):
    def save(self, commit=True):
        instance = super(forms.ModelForm, self).save(commit=False) #inherit as original save() from vanila forms
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