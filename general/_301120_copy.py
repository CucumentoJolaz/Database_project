from django.shortcuts import render, redirect
from django.conf import settings
from general.models import excelFolder, excelFile, rawMaterialsTable, equipmentTable, subcomponentsTable
from general.forms import excelFileForm, excelFolderForm, subcomponentsTableForm
from django.http import Http404, HttpResponse
from general.functions import pathCalculation
from django.views.generic import CreateView
from django.urls import reverse_lazy


# функция генерации случайных номеров, без проверки их уникальности


def test(request):
    return HttpResponse("Test")


def home(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    else:
        return render(request, 'home.html')


# функция для отображения файловой структуры
def prFold(request, **kwargs):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    else:
        # this function is supposed to calculate three variables - full path to the folder, it's name and name + path.
        folderUID, folderPath, fullPath = pathCalculation(**kwargs)
        # checking if this folder does actually exists
        theFolderObject = excelFolder.objects.get(UID=folderUID, path=folderPath)
        # if not - return not found error
        if bool(kwargs):  # if this folder is not the primal one
            if not theFolderObject:
                raise Http404("A folder does not exist")
        # taking all files, folders and tables, which lies inside of the folder
        folders = excelFolder.objects.filter(path=fullPath).order_by('title')
        files = excelFile.objects.filter(path=fullPath).order_by('title')
        # checking if this folder contains any table inside of it
        # and taking table data if it is
        tables = ""
        if theFolderObject.tableName:
            if theFolderObject.tableName == "equipmentTable":
                tables = equipmentTable.objects.filter(parentFolder=theFolderObject)

            elif theFolderObject.tableName == "rawMaterialsTable":
                tables = rawMaterialsTable.objects.filter(parentFolder=theFolderObject)

            elif theFolderObject.tableName == "subcomponentsTable":
                tables = subcomponentsTable.objects.filter(parentFolder=theFolderObject)

        # file download form
        form = excelFileForm(initial={'path': fullPath})
        # folder creation form
        folderForm = excelFolderForm(initial={'path': fullPath}, )
        # html file render with all data inside of the dictinary needed to generate a page

        return render(request, 'general/prFold.html', {
            'folders': folders,  # all directories inside of this directory
            'excelFileForm': form,  # file download form
            'excelNewFolderForm': folderForm,  # folder creation form
            'foldPath': fullPath,  # full path to this directory
            'files': files,  # all files inside of this directory
            'folderTitle': theFolderObject.title,
            'tables': tables,
            'tableType': theFolderObject.tableName,
        })


# Метод для обработки формы на prFold для создания новой папки
def newExcelFolder(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    else:
        if request.method == 'POST':
            print(request.POST['path'])
            form = excelFolderForm(request.POST)
            print(form.errors)
            if form.is_valid():
                form.save(author=request.user.get_username())
            else:
                print("Form is not valid")

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
                # создаём форму для создания папки на сервере и сохраняем её, создавая папку в указанном месте
                # folderModel = excelFolder(title=fileTitle,
                #                          author=request.user.get_username(),
                #                          path=request.POST['path'])
                # folderModel.save()
                # print(form.folderPath)
                form.save(title=fileTitle,
                          author=request.user.get_username(),
                          # UID = getUID(),
                          )
            else:
                print("Form is not valid")
            # перенаправление со страницы загрузки на страницу откуда была вызвана функция
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
                book.delete()
            elif type == 'folder':
                book = excelFolder.objects.get(pk=pk)
                book.delete()
            else:
                return redirect('home')

        return redirect("/" + request.POST['path'])


def renameExcelFile(request, pk):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    else:
        if request.method == 'POST':
            book = excelFile.objects.get(pk=pk)
            book.rename(request.POST['newTitle'])
        return redirect("/" + request.POST['path'])


def renameExcelFolder():
    pass


def createTableView(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    else:
        if request.method == 'GET':
            form = subcomponentsTableForm(initial={'path': request.path})
            return render(request, 'general/../templates/tables/createTableTemplate.html', {
                'form': form,
            })
        if request.method == 'POST':
            form = subcomponentsTableForm(request.POST, request.FILES,)
            if form.is_valid():
                form.save(author=request.user.get_username())
            else:
                print("Form is not valid")
            return redirect(request.POST['path'])
        else:
            return redirect('home')