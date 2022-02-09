import string
import random
from django.http import Http404
from general.models import UIDlist, excelFolder
from abc import ABC, abstractmethod


def getUID(length=6):
    """UID generator"""
    a = "23456789ABCDEFGHJKLMNOPQRSTUVWXYZ"
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


class LinkTreeGenerator(ABC):
    def getLinksUIDsTree(self, folderUID):
        """return list of tuples with names and links
        for folders generator. Supposed to be included to prFold template"""
        foldersTree = self.getFolderTree(folderUID=folderUID)
        return self.generateLinksUIDsTree(foldersTree)

    def getFolderTree(self, folderUID):
        """Checking if the folder defined by folder path and folder UID contains any type of info-tables,
        like equipment, material or other, and returns whole folders tree"""

        # Searching for info in database about the main folder
        foldersTree = []
        theFolderObjects = excelFolder.objects.filter(UID=folderUID)

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

    def generateLinksUIDsTree(self, foldersTree):
        titles = [folder.title for folder in foldersTree]
        UIDs = [folder.UID for folder in foldersTree if folder.UID != 'prFold']
        titles.reverse()
        UIDs.reverse()
        links = [""] + [UID for UID in UIDs]
        # how to insert into a template:
        # {% for title, link in titlesLinks %}
        # {% 'prFold' %}{{ link }}
        # {% endfor %}
        outList = [(title, link) for title, link in zip(titles, links)]
        return outList


class prFoldLinkTreeGenerator(LinkTreeGenerator):
    pass
