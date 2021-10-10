from django.shortcuts import render, redirect
from django.conf import settings
from django.http import Http404, HttpResponse, HttpResponseNotFound
from django.core.files.storage import FileSystemStorage
import mimetypes
from general.models import excelFolder, excelFile
from general.forms import excelFileForm, excelFolderForm
import general.functions as genFunc



# функция генерации случайных номеров, без проверки их уникальности


def test(request):
    return HttpResponse("Test")


def home(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    else:
        return render(request, 'home.html')


# main folder evaluation
def prFold(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    else:
        # this function is supposed to calculate three variables - full path to the folder, it's name and name + path.
        folderUID, folderPath, fullPath = genFunc.pathCalculation(**kwargs)
        # Handling main folder structure
        theFolderObject = genFunc.mainFoldStruct(folderUID = folderUID, folderPath = folderPath)
        # checking if main folder contains any table inside
        # and taking table data if it is
        tables = genFunc.getTablesInfo(theFolderObject)
        #handling info about files and folders inside of the main folder
        folders = excelFolder.objects.filter(path=fullPath).order_by('title')
        files = excelFile.objects.filter(path=fullPath).order_by('title')
        #file upload and new folder creation in main forder forms
        # handling all files, folders and tables, which lies inside of the main folder
        fileForm = excelFileForm(initial={'path': fullPath})
        folderForm = excelFolderForm(initial={'path': fullPath, 'author': request.user.get_username()}, )
        return render(request, 'general/prFold.html', {
            'folders': folders,  # all directories inside of this directory
            'excelFileForm': fileForm,  # file download form
            'excelNewFolderForm': folderForm,  # folder creation form
            'foldPath': fullPath,  # full path to this directory
            'files': files,  # all files inside of this directory
            'folderTitle': theFolderObject.title,
            'tables': tables,
            'tableType': theFolderObject.tableName,
            'previousFolder': folderPath,  # path to previous directory
        })


# Form creation function for new folders
def newExcelFolder(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    else:
        if request.method == 'POST':
            form = excelFolderForm(request.POST)
            if form.is_valid():
                form.save()
            else:
                print(form.is_valid())
            return redirect(request.POST['path'])
        else:
            return redirect('home')


def uploadExcelFile(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    else:
        if request.method == 'POST':
            fileTitle = request.FILES['file'].name
            form = excelFileForm(request.POST, request.FILES, )
            if form.is_valid():
                form.save(title=fileTitle,
                          author=request.user.get_username(),
                          )
            else:
                print("Form is not valid")
            return redirect(request.POST['path'])
        else:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))


def deleteExcel(request, pk, type):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    else:
        if request.method == 'POST':
            if type == 'file':
                book = excelFile.objects.get(pk=pk)
                book.falseDeletion()
            elif type == 'folder':
                book = excelFolder.objects.get(pk=pk)
                book.falseDeletion()
            else:
                return redirect('home')

        return redirect("/" + request.POST['path'])


def renameExcelFile(request, pk):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    else:
        if request.method == 'POST':
            book = excelFile.objects.get(pk=pk)
            if request.POST['newTitle'] != "":
                book.rename(request.POST['newTitle'])
            if request.POST['additionalInfo'] != "":
                book.additionalInfo = request.POST['additionalInfo']
                book.save()
        return redirect("/" + request.POST['path'])


def renameExcelFolder(request, pk):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    else:
        if request.method == 'POST':
            if request.POST['newTitle'] != "":
                book = excelFolder.objects.get(pk=pk)
                book.rename(request.POST['newTitle'])
        return redirect("/" + request.POST['path'])


def downloadExcelFile(request, pk):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    else:
        file = excelFile.objects.get(pk=pk)
        fileName = file.title
        filePath = file.path + "/" + file.UID
        mime_type, _ = mimetypes.guess_type(filePath)
        fs = FileSystemStorage()
        if fs.exists(filePath):
            with fs.open(filePath) as file:
                response = HttpResponse(file, content_type=mime_type)
                response['Content-Disposition'] = 'attachment; filename="' + fileName + '"'
                return response
        else:
            return HttpResponseNotFound('The file wasnt found at the server')

        return redirect("/" + file.path)
