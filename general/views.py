from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponseNotFound

from general.functions.views.delete import processDelete
from general.functions.views.download import processDownloadFile
from general.functions.views.new_folder import processNewFolder, initialiseNewFolder
from general.functions.views.prFold_init import initialisePrFold
from general.functions.views.rename import processRenameFile, processRenameFolder
from general.functions.views.upload_file import processUploadFile, initialiseUploadFile
from general.models import excelFolder


@login_required
def home(request):
    """
    Home template rendering.
    home(request):
    """
    return render(request, "home.html")


@login_required
def prFold(request, **kwargs):
    """
    Accept a request and render excelFolder HTML page.
    prFold(request, **kwargs)
    """
    folderUID = kwargs.get("fold_uid", "prFold")
    renderDict = initialisePrFold(theFolderObject=excelFolder.objects.get(UID=folderUID))
    return render(request, "general/prFold.html", renderDict)


@login_required
def newExcelFolder(request):
    """
    If request is POST type - Creating new folder, if request is appropriate;
    If request is GET type - initialising appropriate data from request, combine it to
    render dictionary, and render if in general/createFolder.html.
    newExcelFolder(request)
    """
    if request.method == "POST":
        processNewFolder(request)
        return redirect(request.POST['pathBack'])

    if request.method == "GET":
        renderDict = initialiseNewFolder(request)
        return render(request, "general/createFolder.html", renderDict)


@login_required
def uploadExcelFile(request):
    """
    If request is POST type - uploading new file, if request is appropriate;
    If request is GET type - initialising appropriate data from request, combine it to
    render dictionary, and render if in general/uploadFile.html.
    uploadExcelFile(request)
    """
    if request.method == "POST":
        processUploadFile(request)
        return redirect(request.POST['pathBack'])

    if request.method == "GET":
        renderDict = initialiseUploadFile(request)
        return render(request, "general/uploadFile.html", renderDict)


@login_required
def deleteExcel(request, **kwargs):
    """
    Deletion view for folder of file by request, Only POST.
    deleteExcel(request, **kwargs)
    """
    if request.method == "POST":
        processDelete(**kwargs)
        return redirect(f"/{request.POST['pathBack']}")


@login_required
def renameExcelFile(request, **kwargs):
    """
    View for renaming and changing additionalInfo of excelFile instance.
    renameExcelFile(request, **kwargs)
    """
    if request.method == 'POST':
        processRenameFile(request, **kwargs)
        return redirect(f"/{request.POST['pathBack']}")


@login_required
def renameExcelFolder(request, **kwargs):
    """
    View for renaming  of excelFolder instance.
    renameExcelFile(request, **kwargs)
    """
    if request.method == 'POST':
        processRenameFolder(request, **kwargs)
        return redirect(f"/{request.POST['pathBack']}")


@login_required
def downloadExcelFile(request, **kwargs):
    """
    View for downloading file from cloud server/database.
    downloadExcelFile(request, **kwargs)
    """
    downloadedFile = processDownloadFile(**kwargs)
    if downloadedFile:
        return downloadedFile
    else:
        return HttpResponseNotFound('The file was not found at the server')
