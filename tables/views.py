from django.conf import settings
from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect, get_object_or_404

import tables.tableCheckFunctions as tc
from general.forms import excelFileForm
from general.models import excelFile


def createProcessingView(request, **kwargs):
    """creating new instance of table"""
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    else:
        tableInfoProc = tc.tableInfoProcessor()

        viewForm = tableInfoProc.tableTypeForm(kwargs['tableType'])
        if request.method == 'POST':
            formData = viewForm(request.POST)
            if formData.is_valid():
                formData.path = request.POST['path']
                formData.save(author=request.user.get_username())
            return redirect("/" + request.POST['pathBack'])

        formData = viewForm()
        if 'path' in request.GET and 'pathBack' in request.GET:
            return render(request, 'tables/createTableTemplate.html', {'form': formData,
                                                                       'path': request.GET['path'],
                                                                       'pathBack': request.GET['pathBack']})
        else:
            return redirect('home')


def updateProcessingView(request, **kwargs):
    """Updating table instance"""
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    else:
        tableInfoProc = tc.tableInfoProcessor()

        viewForm = tableInfoProc.tableTypeFormUpdate(kwargs['tableType'])
        viewModel = tableInfoProc.tableTypeModel(kwargs['tableType'])

        if request.method == 'POST':
            instance = get_object_or_404(viewModel, UID=kwargs['UID'])
            form = viewForm(request.POST, instance=instance)
            updateMessage="Не получилось обновить компонент."
            if form.is_valid():
                form.save()
                updateMessage="Компонент успешно обновлён!"
            return redirect(f"/{request.POST['pathBack']}?updateMessage={updateMessage}")

        if request.method == 'GET':
            modelData = viewModel.objects.get(UID=kwargs['UID'])
            form = viewForm(instance=modelData)
            renderDict = {'path': f"tables/update/{kwargs['tableType']}/{modelData.UID}",
                          'pathBack': f"{modelData.path}",
                          'fileUploadPath': f"{modelData.path}/{modelData.UID}",

                          'excelFileForm': excelFileForm,
                          'files': excelFile.objects.filter(path=f"{modelData.path}/{modelData.UID}").order_by('title'),
                          'object': modelData,
                          'form': form,
                          'tableTypeRedirect': kwargs['tableType'],
                          'updateMessage': request.GET.get('updateMessage', '')
                          }
            return render(request, 'tables/updateTableTemplate.html', renderDict)


def deleteProcessingView(request, **kwargs):
    """Deleting table instance"""
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    else:
        tableInfoProc = tc.tableInfoProcessor()

        viewModel = tableInfoProc.tableTypeModel(kwargs['tableType'])
        if request.method == 'POST':
            modelData = viewModel.objects.get(UID=kwargs.get('UID'))
            modelData.falseDeletion()

        return redirect("/" + request.POST['pathBack'])

def approveTable(request, tableType, pk):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    else:
        if request.method == 'POST':
            tableInfoProc = tc.tableInfoProcessor()

            table = tableInfoProc.tableTypeModel(tableType)
            if table:
                query = table.objects.filter(pk=pk)
                if query:
                    objectToApprove = query[0]
                    objectToApprove.approved = True
                    objectToApprove.save()
                    return redirect(request.POST['pathBack'])
                else:
                    return HttpResponseNotFound("Object not found.")
            else:
                return HttpResponseNotFound("Wrong table type request.")
