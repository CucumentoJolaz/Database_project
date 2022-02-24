from django import forms

from tables.models import statusTable

class changeStatusForm(forms.ModelForm):
    class Meta:
        model = statusTable
        fields = ('title',)

    title = forms.ModelChoiceField(
        queryset=statusTable.objects.filter(deleted=False),
        label="Выберите новый статус",
    )