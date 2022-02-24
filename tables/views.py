from django.core.exceptions import PermissionDenied, ValidationError
from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

import tables.functions.table_check as tc
from tables.functions.view_checks import checkStatusPermissions, checkIfCanUpdate
from tables.models import statusTable
from tables.forms.misc_forms import changeStatusForm
from general.forms import excelFileForm
from general.models import excelFile
from tables.functions.tree_folders import tablesLinkTreeGenerator
import general.functions.tree_folders as genFunc


@login_required
def createProcessingView(request, **kwargs):
    """
    creating new instance of table
    createProcessingView(request, **kwargs)
    """
    tableInfoProc = tc.tableInfoProcessor()

    viewForm = tableInfoProc.tableTypeFormCreate(kwargs['tableType'])
    if request.method == 'POST':
        formData = viewForm(request.POST)
        if formData.is_valid():
            formData.save(author=request.user, path=request.POST['path'])
        else:
            print(formData.errors)
        return redirect("/" + request.POST['pathBack'])

    formData = viewForm()
    if 'path' in request.GET and 'pathBack' in request.GET:
        tg = genFunc.prFoldLinkTreeGenerator()
        treeTitlesLinks = tg.getLinksUIDsTree(folderUID=request.GET['path'].split("/")[-1])
        return render(request, 'tables/createTable.html', {'form': formData,
                                                           'path': request.GET['path'],
                                                           'pathBack': request.GET['pathBack'],
                                                           'treeTitlesLinks': treeTitlesLinks})
    else:
        return redirect('home')


@login_required
def updateProcessingView(request, **kwargs):
    """
    Updating table instance
    updateProcessingView(request, **kwargs)
    """
    tableInfoProc = tc.tableInfoProcessor()
    viewModel = tableInfoProc.tableTypeModel(kwargs['tableType'])

    if request.method == 'POST':
        instance = get_object_or_404(viewModel, UID=kwargs['UID'])
        viewForm = tableInfoProc.tableTypeFormUpdate(kwargs['tableType'])
        form = viewForm(request.POST, instance=instance)
        updateMessage = "Не получилось обновить компонент."
        if form.is_valid():
            form.save()
            updateMessage = "Компонент успешно обновлён!"
        else:
            print(form.errors)
        return redirect(f"/{request.POST['pathToInstance']}?updateMessage={updateMessage}")

    if request.method == 'GET':
        modelData = viewModel.objects.get(UID=kwargs['UID'])
        updateMessage = ""

        # if instance has a status, like rawMaterial or Component
        if "status_id" in modelData.__dict__:
            statusForm = changeStatusForm(initial={'field1': statusTable.getDefaultPk()})
            canUpdate = checkIfCanUpdate(request, modelData.status)
        else:
            statusForm = None
            canUpdate = checkIfCanUpdate(request)

        # if updateProcessingView requested to update an instance
        if "update" in request.GET:
            if canUpdate:
                viewForm = tableInfoProc.tableTypeFormUpdate(kwargs['tableType'])
                updateTemp = True
            else:
                viewForm = tableInfoProc.tableTypeFormDemo(kwargs['tableType'])
                updateMessage = "Вы не имеете права редактировать данный компонент."
                updateTemp = False
        else:
            viewForm = tableInfoProc.tableTypeFormDemo(kwargs['tableType'])
            updateTemp = False

        form = viewForm(instance=modelData)
        treeTitlesLinksGenerator = tablesLinkTreeGenerator(tableType=kwargs['tableType'])
        treeTitlesLinks = treeTitlesLinksGenerator.getLinksUIDsTreeTable(tableUID=kwargs['UID'])

        if not updateMessage:
            updateMessage = request.GET.get('updateMessage', '')
        renderDict = {'excelFileForm': excelFileForm,
                      'files': excelFile.objects.filter(path=f"{modelData.path}/{modelData.UID}").order_by('title'),
                      'object': modelData,
                      'form': form,
                      'tableTypeRedirect': kwargs['tableType'],
                      'updateMessage': updateMessage,
                      "treeTitlesLinks": treeTitlesLinks,
                      "statusForm": statusForm,
                      "canUpdate": canUpdate,
                      "updateTemp": updateTemp,
                      }
        return render(request, 'tables/updateTable.html', renderDict)


@login_required
def deleteProcessingView(request, **kwargs):
    """
    Deleting table instance
    deleteProcessingView(request, **kwargs):
    """
    tableInfoProc = tc.tableInfoProcessor()

    viewModel = tableInfoProc.tableTypeModel(kwargs['tableType'])
    if request.method == 'POST':
        modelData = viewModel.objects.get(UID=kwargs.get('UID'))
        modelData.falseDeletion()

    return redirect(request.POST['pathToParentFolder'])


@login_required
def changeStatusView(request, **kwargs):
    """
    Changing status of the table instance;
    changeStatusView(request, **kwargs):
    """

    if request.method == 'POST':
        tableInfoProc = tc.tableInfoProcessor()
        table = tableInfoProc.tableTypeModel(kwargs['tableType'])
        if table:
            query = table.objects.filter(UID=kwargs['UID'])
            if query:
                modelData = query[0]
                status_id = request.POST['title']  # getting id of the status
                statusObj = statusTable.objects.get(pk=status_id)
                try:
                    checkStatusPermissions(request, statusObj)
                    modelData.status = statusObj
                    modelData.save()
                    updateMessage = "Статус успешно изменён"
                except PermissionDenied:
                    updateMessage = "У вас нет прав для изменения статуса на данный"
                return redirect(f"/{request.POST['pathToInstance']}?updateMessage={updateMessage}")
            else:
                return HttpResponseNotFound("Object not found.")
        else:
            return HttpResponseNotFound("Wrong table type request.")


