import string
import random
from django.shortcuts import redirect
from django.http import Http404
from general.models import UIDlist, excelFolder
from tables.models import equipmentTable, rawMaterialsTable, subcomponentsTable, organisationTable, statusTable, \
    measurementUnitTable


def getUID(length=6):
    """UID generator"""
    a = string.ascii_uppercase
    a += string.digits
    list1 = []
    list1[:0] = a
    UID = ""

    while True:
        for i in range(length):
            UID += list1[random.randint(0, len(list1) - 1)]
        if not UIDlist.objects.filter(UID=UID):
            q = UIDlist(UID=UID)
            q.save()
            break
        else:
            UID = ""
    return UID


def pathCalculation(**kwargs):
    """function for calculation of the whole folder path """
    pathToFolder = ""
    for key, value in kwargs.items():
        pathToFolder += value + "/"
    pathToFolder = pathToFolder[:-1]  # delete the last slash
    folderUID = pathToFolder.rsplit("/")[-1]  # name of the folder, which we need to display
    folderPath = ""
    if len(kwargs) == 0:
        fullPath = folderUID = "prFold"
    elif len(kwargs) == 1:
        folderPath = "prFold"
        fullPath = folderPath + "/" + folderUID
    else:
        folderPath = "prFold/" + pathToFolder.replace(folderUID, "")[
                                 :-1]  # The folder in which another folder is placed
        fullPath = folderPath + "/" + folderUID

    return (folderUID, folderPath, fullPath)


def mainFoldStruct(folderUID, folderPath):
    """Checking if the folder defined by folder path and folder UID contains any type of info-tables,
    like equipment, material or other, and returns whole folders tree"""

    # Searching for info in database about the main folder
    foldersTree = []
    theFolderObjects = excelFolder.objects.filter(UID=folderUID, path=folderPath)
    if theFolderObjects:
        i = 0
        foldersTree.append(theFolderObjects[0])
        while foldersTree[i].parentFolder is not None:
            parentFolder = excelFolder.objects.filter(id=foldersTree[i].parentFolder.id)
            foldersTree.append(parentFolder[0])
            i += 1

    if not foldersTree:
        raise Http404("There is no such folder")

    return foldersTree


def namesLinksFolder(foldersTree):
    """return list of tuples with names and links
    for folders generator. Supposed to be included to prFold template"""

    titles = [folder.title for folder in foldersTree]
    UIDs = [folder.UID for folder in foldersTree if folder.UID != 'prFold']
    titles.reverse()
    UIDs.reverse()
    links = ["/".join(UIDs[:i + 1]) for i, UID in enumerate(UIDs)]
    links = [""] + links
    # how to insert into a template:
    # {% for title, link in titlesLinks %}
    # {% 'prFold' %}{{ link }}
    # {% endfor %}
    outList = [(title, link) for title, link in zip(titles, links)]
    return outList
