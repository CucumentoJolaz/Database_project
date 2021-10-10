import string
import random
from django.shortcuts import redirect
from django.http import Http404
from general.models import UIDlist, excelFolder
from tables.models import equipmentTable, rawMaterialsTable, subcomponentsTable
#function UId generator
def getUID(length = 8):
    a = string.ascii_uppercase
    a += string.digits
    list1 = []
    list1[:0] = a
    UID = ""

    while True:
        for i in range(length):
            UID += list1[random.randint(0, len(list1) - 1)]
        if not UIDlist.objects.filter(UID = UID):
            q = UIDlist(UID=UID)
            q.save()
            break
        else:
            UID = ""
    return UID

#function for calculation of folder path at cite
def pathCalculation(**kwargs):
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
        folderPath = "prFold/" + pathToFolder.replace(folderUID, "")[:-1]  # The folder in which another folder is placed
        fullPath = folderPath + "/" + folderUID

    return (folderUID, folderPath, fullPath)


def getTablesInfo(theFolderObject):
    if theFolderObject.tableName:
        if theFolderObject.tableName == "equipmentTable":
            table = equipmentTable
        elif theFolderObject.tableName == "rawMaterialsTable":
            table = rawMaterialsTable
        elif theFolderObject.tableName == "subcomponentsTable":
            table = subcomponentsTable
        return table.objects.filter(parentFolder=theFolderObject)

def mainFoldStruct(folderUID, folderPath):
    # object, name, redirect
    typeOfFolders = [{'object': excelFolder, 'name': 'folder', 'redirect': ''},
                     {'object': equipmentTable, 'name': 'An equipment', 'redirect': 'updateEquipment/'},
                     {'object': rawMaterialsTable, 'name': 'A rawMaterial', 'redirect': 'updateRawMaterial/'},
                     {'object': subcomponentsTable, 'name': 'A subcomponent', 'redirect': 'updateSubcomponent/'}]

    # Searching for info in database about main folder
    theFolderObject = ""
    for foldInfo in typeOfFolders:
        theFolderObjects = foldInfo['object'].objects.filter(UID=folderUID, path=folderPath)
        if theFolderObjects:
            theFolderObject = theFolderObjects[0]
            if foldInfo['name'] != 'folder':
                redirect("/tables/" + foldInfo['redirect'] + str(
                    theFolderObjects[0].pk))
    if not theFolderObject:
        raise Http404("There is no such folder")
    return theFolderObject