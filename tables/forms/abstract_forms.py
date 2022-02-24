from django import forms
from django.contrib.auth.models import User

from general.forms import abstractFolderForm
from tables.models import subcomponentsTable, rawMaterialsTable, organisationTable, measurementUnitTable, \
    equipmentTable, \
    statusTable, documentTypeTable, departmentTable, documentTable
from tables.widgets import XDSoftDateTimePickerInput, XDSoftTimePickerInput

defaultChoiceList = 'Не указана'


# creating N different kind of forms, which supposed to display a form to
# create an instance of it's model



class somethingChoice(forms.ModelChoiceField):

    def label_from_instance(self, somethingObj):
        if "title" in somethingObj.__dict__:
            return f'{somethingObj.title}'
        elif "nickname" in somethingObj.__dict__:
            return f'{somethingObj.nickname}'

class initForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(forms.ModelForm, self).__init__(*args, **kwargs)
        self.fields['description'].widget.attrs.update({'class': 'descriptionInput'})
        # for field in self.fields.values():
        #     field.widget.attrs.update({'class': 'formInputStyleTable'})
        #
        # self.fields['description'].widget.attrs.update({'class': 'formInputStyleTable descriptionInput'})

    title = forms.CharField(label='Название')
    description = forms.CharField(widget=forms.Textarea,
                                  label='Описание',
                                  required=False)

class subcomponentsTableForm(initForm):
    class Meta:
        model = subcomponentsTable
        fields = ('title',
                  'originalAmount', 'availableAmount',
                  'creationTime', 'cost', 'path', 'description')

        widgets = {
            'path': forms.HiddenInput(), }

    originalAmount = forms.FloatField(label='Искодное количество')
    availableAmount = forms.FloatField(label='Актуальное количество')
    creationTime = forms.TimeField(label='Время создания',
                                   widget=forms.TimeInput(
                                       attrs={'type': 'time'}, ))  # , widget=XDSoftTimePickerInput())
    cost = forms.FloatField(label='Цена')


class rawMaterialsTableForm(initForm):
    class Meta:
        model = rawMaterialsTable
        fields = ['title',
                  'originalAmount', 'availableAmount',
                  'cost',
                  'measurementUnit', 'serialNumber',
                  'organisation', 'path', 'description']
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


class equipmentTableForm(initForm):
    class Meta:
        model = equipmentTable
        fields = ('title',
                  'productivity', 'exploitationCost',
                  'serialNumber',
                  'organisation', 'path', 'description')
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


class measurementUnitTableForm(initForm):
    class Meta:
        model = measurementUnitTable
        fields = ('title',
                  'description', 'path')
        widgets = {
            'path': forms.HiddenInput(),
        }


class statusTableForm(initForm):
    class Meta:
        model = statusTable
        fields = ('title',
                  'description', 'path')
        widgets = {
            'path': forms.HiddenInput(),
        }


class organisationTableForm(initForm):
    class Meta:
        model = organisationTable
        fields = ('title',
                  'description', 'path',
                  'address')
        widgets = {
            'path': forms.HiddenInput(),
        }

    address = forms.CharField(label='Юридический адрес')


class documentTableForm(initForm):
    class Meta:
        model = documentTable
        fields = ('title',
                  'description', 'path',
                  'coAuthor', 'reviewer',
                  'documentType', 'checkUntil',
                  'approveUntil')
        widgets = {
            'path': forms.HiddenInput(),
        }

    coAuthor = forms.ModelChoiceField(
        queryset=User.objects.filter(is_active=True, is_superuser=False),
        required=False,
        label='Соавтор',
    )
    reviewer = forms.ModelChoiceField(
        queryset=User.objects.filter(is_active=True, is_superuser=False),
        required=False,
        label='Ревьюер',
    )
    documentType = somethingChoice(
        queryset=documentTypeTable.objects.filter(deleted=False),
        required=False,
        label='Тип документа',
    )
    checkUntil = forms.DateTimeField(label='Проверить до',
                                     #input_formats=['%d/%m/%Y %H:%M'],
                                     widget=XDSoftDateTimePickerInput(),
                                     )
    # widget=forms.DateTimeInput(
    #     attrs={'type': 'datetime-local'},
    #     format='%d/%m/%Y %H:%M'))
    approveUntil = forms.DateTimeField(label='Утвердить до',
                                       #input_formats=['%d/%m/%Y %H:%M'],
                                       widget=XDSoftDateTimePickerInput())  # widget=XDSoftDateTimePickerInput()


class departmentTableForm(initForm):
    class Meta:
        model = departmentTable
        fields = ('title',
                  'description', 'path')
        widgets = {
            'path': forms.HiddenInput(),
        }


class documentTypeTableForm(initForm):
    class Meta:
        model = documentTypeTable
        fields = ('title',
                  'description', 'path')
        widgets = {
            'path': forms.HiddenInput(),
        }
