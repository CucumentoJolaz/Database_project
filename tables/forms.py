from general.forms import excelFolderForm
from tables.models import subcomponentsTable, rawMaterialsTable, equipmentTable, organisationTable, \
    measurementUnitTable, statusTable
from django import forms

defaultChoiceList = 'Не указана'


class somethingChoice(forms.ModelChoiceField):

    def label_from_instance(self, somethingObj):
        return f'{somethingObj.title}'


class defaultTableForm(excelFolderForm):
    def __init__(self, *args, **kwargs):
        super(excelFolderForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'formInputStyleTable'})

        self.fields['description'].widget.attrs.update({'class': 'formInputStyleTable descriptionInput'})

    title = forms.CharField(label='Название')
    description = forms.CharField(widget=forms.Textarea, label='Описание')

# creating 6 different kind of forms, which supposed to display a form to
# create an instance of it's model
# inheritance from excelFolderForm was made to inherit save() function
class subcomponentsTableForm(defaultTableForm):
    class Meta:
        model = subcomponentsTable
        fields = ('title',
                  'originalAmount', 'availableAmount',
                  'creationTime', 'cost', 'path')

        widgets = {
            'path': forms.HiddenInput(), }

    originalAmount = forms.FloatField(label='Искодное количество')
    availableAmount = forms.FloatField(label='Актуальное количество')
    creationTime = forms.TimeField(label='Время создания')
    cost = forms.FloatField(label='Цена')


class rawMaterialsTableForm(defaultTableForm):
    class Meta:
        model = rawMaterialsTable
        fields = ['title',
                  'originalAmount', 'availableAmount',
                  'cost',
                  'measurementUnit', 'serialNumber',
                  'organisation', 'path']
        widgets = {
            'path': forms.HiddenInput(), }

    originalAmount = forms.FloatField(label='Искодное количество')
    availableAmount = forms.FloatField(label='Актуальное количество')
    cost = forms.FloatField(label='Цена')
    serialNumber = forms.CharField(label='Серийный номер')

    organisation = somethingChoice(
        queryset=organisationTable.objects.filter(deleted=False),
        required=False,
        label='Организация',
        empty_label=defaultChoiceList
    )

    measurementUnit = somethingChoice(
        queryset=measurementUnitTable.objects.filter(deleted=False),
        required=False,
        label='Единица измерения',
        empty_label=defaultChoiceList
    )


class equipmentTableForm(defaultTableForm):
    class Meta:
        model = equipmentTable
        fields = ('title',
                  'productivity', 'exploitationCost',
                  'serialNumber',
                  'organisation', 'path')
        widgets = {
            'path': forms.HiddenInput(),
        }

    productivity = forms.FloatField(label='Продуктивность')
    exploitationCost = forms.FloatField(label='Цена эксплуатации')
    serialNumber = forms.CharField(label='Серийный номер')

    organisation = somethingChoice(
        queryset=organisationTable.objects.filter(deleted=False),
        required=False,
        label="Организация",
        empty_label=defaultChoiceList
    )


class measurementUnitTableForm(defaultTableForm):
    class Meta:
        model = measurementUnitTable
        fields = ('title',
                  'description', 'path')
        widgets = {
            'path': forms.HiddenInput(),
        }


class statusTableForm(defaultTableForm):
    class Meta:
        model = statusTable
        fields = ('title',
                  'description', 'path')
        widgets = {
            'path': forms.HiddenInput(),
        }


class organisationTableForm(defaultTableForm):
    class Meta:
        model = organisationTable
        fields = ('title',
                  'description', 'path',
                  'address')
        widgets = {
            'path': forms.HiddenInput(),
        }

    address = forms.CharField(label='Юридический адрес')


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
