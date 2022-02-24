from django import forms
from .models import excelFolder, excelFile
from general.functions.tree_folders import getUID
from general.functions.db_init import createDir


class NameForm(forms.Form):
    your_name = forms.CharField(label='your name', max_length=100)


class ContactForm(forms.Form):
    subject = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)
    sender = forms.EmailField()
    cc_myself = forms.BooleanField(required=False)


class abstractFolderForm(forms.ModelForm):
    def save(self, author, path="ghost", tableName="", commit=True):
        instance = super(abstractFolderForm, self).save(commit=False)
        newUID = getUID()
        instance.UID = newUID
        instance.author = author
        instance.path = path
        instance.tableName = tableName
        createDir("/".join([instance.path, newUID]))
        q = excelFolder.objects.get(UID=instance.path.rsplit("/")[-1])  # ищем ту директорию, в которую созраняется файл
        instance.parentFolder = q  # присваиваем файл к данной директории
        if commit:
            instance.save()
        return instance


class excelFileForm(forms.ModelForm):
    class Meta:
        model = excelFile
        fields = ('file', 'path')
        widgets = {'path': forms.HiddenInput()}

    def save(self, author, title, commit=True):
        instance = super(excelFileForm, self).save(commit=False)
        instance.title = title
        instance.author = author
        instance.UID = getUID()
        instance.parentFolderUID = instance.path.split("/")[-1]
        instance.file.filename = instance.UID
        if commit:
            instance.save()
        return instance


class excelFolderForm(abstractFolderForm):
    def __init__(self, *args, **kwargs):
        super(abstractFolderForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'formInputStyleTable'})

        self.fields['description'].widget.attrs.update({'class': 'formInputStyleTable descriptionInput'})

    title = forms.CharField(label='Название')
    description = forms.CharField(widget=forms.Textarea,
                                  label='Описание',
                                  required=False)

    class Meta:
        model = excelFolder
        fields = ('title', 'description')
