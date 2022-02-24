from general.forms import excelFolderForm, excelFileForm
from general.models import excelFolder, excelFile

import general.functions.tree_folders as genFunc
import tables.functions.table_check as tc


def prFoldInitialise(theFolderObject: excelFolder) -> dict:
    """
    Gets folder instance and returns appropriate dictionary with forms
    def prFoldInitialise(theFolderObject: excelFolder) -> dict
    """

    if theFolderObject.UID != 'prFold':
        previousFolder = f"prFold/{theFolderObject.parentFolder.UID}"
        pathBack = f"prFold/{theFolderObject.UID}"
        fullPath = f"{theFolderObject.path}/{theFolderObject.UID}"
    else:
        previousFolder = ""
        pathBack = "prFold"
        fullPath = "prFold"

    tg = genFunc.prFoldLinkTreeGenerator()
    treeTitlesLinks = tg.getLinksUIDsTree(folderUID=theFolderObject.UID)
    # checking if main folder contains any table inside
    # and taking table data if it is

    tableInfoProc = tc.tableInfoProcessor()
    tables = tableInfoProc.getTables(theFolderObject)
    tableType = theFolderObject.tableName
    # handling info about files and folders inside of the main folder
    folders = excelFolder.objects.filter(parentFolder=theFolderObject).order_by('title')
    files = excelFile.objects.filter(parentFolderUID=theFolderObject.UID).order_by('title')
    folderForm = excelFolderForm()
    fileForm = excelFileForm()

    outDict = {'folders': folders,  # all directories inside of this directory
               'foldPath': fullPath,  # full path to this directory
               'files': files,  # all files inside of this directory
               'tables': tables,  # equipment, materials, organisations etc.
               'previousFolder': previousFolder,  # path to previous directory
               'pathBack': pathBack,  # tell the template it's parent
               'treeTitlesLinks': treeTitlesLinks,
               'tableTypeRedirect': tableType,
               'folderForm': folderForm,
               'fileForm': fileForm, }
    return outDict


