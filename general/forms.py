from django import forms
from .models import excelFolder, excelFile
import os
from config.settings import MEDIA_ROOT
from general.functions import getUID
from general.db_init import createDir

class NameForm(forms.Form):
    your_name = forms.CharField(label='your name', max_length=100)


class ContactForm(forms.Form):
    subject = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)
    sender = forms.EmailField()
    cc_myself = forms.BooleanField(required=False)


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
        instance.file.filename = instance.UID
        if commit:
            instance.save()
        return instance


class excelFolderForm(forms.ModelForm):
    class Meta:
        model = excelFolder
        fields = ('title', 'path', 'author')
        widgets = {
            'path': forms.HiddenInput(),
            'author': forms.HiddenInput(),
            #'path': forms.TextInput(attrs={'placeholder': 'Введите название новой директории'}),
        }

    def save(self, author, commit=True):
        instance = super(excelFolderForm, self).save(commit=False)
        newUID = getUID()
        instance.UID = newUID
        instance.author = author
        createDir("/".join([instance.path, newUID]))
        q = excelFolder.objects.get(UID=instance.path.rsplit("/")[-1])  # ищем ту директорию, в которую созраняется файл
        print(q, type(q))

        instance.parentFolder = q  # присваиваем файл к данной директории
        if commit:
            instance.save()
        return instance


