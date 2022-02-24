from django.db import models
from django.contrib.auth.models import User
import os
import shutil
from config.settings import MEDIA_ROOT


def content_file_name(instance, UID):
    """ this function has to return the location to upload the file """
    return os.path.join('%s/%s' % (instance.path, instance.UID))


class UIDlist(models.Model):
    UID = models.CharField(max_length=300, default="")

    def __str__(self):
        return self.UID


# abstract folder - paternal abstract class for several different instances of data structures in the database cite
class abstractFolder(models.Model):
    class Meta:
        abstract = True

    title = models.CharField(max_length=100)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    path = models.CharField(max_length=300, default="ghost",  blank=True)
    creationDate = models.DateTimeField(auto_now_add=True)
    updateDate = models.DateTimeField(auto_now=True)
    UID = models.CharField(max_length=10, default="")
    tableName = models.CharField(max_length=50,
                                 default="",  blank=True)  # this field tells a folder about table fields, which contains the folder
    deleted = models.BooleanField(default=False)
    description = models.TextField(default="", blank=True)

    def __str__(self):
        return self.title

    # complete removal of all info, files, folders and traces of the folder.
    # use with EXTREME caution, because if someone would like to
    # restore all that info, he/she will need to use special
    # equipment to do so
    def delete(self, *args, **kwargs):
        shutil.rmtree(os.path.join(MEDIA_ROOT, self.path, self.UID))
        # Removal of the all directories, which the directory contain
        folderDeletion = excelFolder.objects.filter(path__startswith=self.path + "/" + self.UID)
        # Removal of the all files, which the directory contain
        fileDeletion = excelFile.objects.filter(path__startswith=self.path + "/" + self.UID)
        folderDeletion.delete()
        fileDeletion.delete()
        q = UIDlist.objects.filter(UID=self.UID)
        q.delete()
        super().delete(*args, **kwargs)

    # Just mark a file or folder as "deleted" in database, without, actually, deleting that irreversely
    def falseDeletion(self, *args, **kwargs):
        folders = excelFolder.objects.filter(path__startswith=self.path + "/" + self.UID)
        files = excelFile.objects.filter(path__startswith=self.path + "/" + self.UID)
        for folder in folders:
            folder.falseDeletion()
        for file in files:
            file.falseDeletion()

        # if self.tableName:
        #     tableInfoProc = tc.tableInfoProcessor()
        #     tableModel = tableInfoProc.tableTypeModel(self.tableName)
        #     tables = tableInfoProc.getTables(self)
        #     for table in tables:
        #         table.falseDeletion()

        self.deleted = True
        self.save()

    def rename(self, newTitle):
        self.title = newTitle
        self.save()


class excelFolder(abstractFolder):
    parentFolder = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True)


class excelFile(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    file = models.FileField(upload_to=content_file_name)
    creationDate = models.DateTimeField(auto_now_add=True)
    updateDate = models.DateTimeField(auto_now=True)
    path = models.CharField(max_length=500, default="prFold")
    UID = models.CharField(max_length=10, default="")
    additionalInfo = models.CharField(max_length=1000, default="")
    parentFolderUID = models.CharField(max_length=10, default="")
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def delete(self, *args, **kwargs):
        self.file.delete()
        q = UIDlist.objects.filter(UID=self.UID)
        q.delete()
        super().delete(*args, **kwargs)

    def falseDeletion(self, *args, **kwargs):
        self.deleted = True
        self.save()

    def rename(self, newTitle):
        self.title = newTitle
        self.save()
