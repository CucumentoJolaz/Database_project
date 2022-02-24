from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType

from general.models import excelFolder
from general.functions.tree_folders import getUID
import os
import boto3

from tables.models import statusTable


def createDir(title):
    """Directory creation in S3 amazon bukkit through boto3"""
    BUCKET_NAME = os.environ.get('S3_BUCKET_NAME')
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(BUCKET_NAME)
    Key = title + "/"
    bucket.put_object(Key=Key)


def dbCheckInit():
    """Checking if the database was initialised properly"""
    if len(excelFolder.objects.filter(UID="ghost") | excelFolder.objects.filter(UID="prFold")) == 2:
        return True


def dbInit():
    """Initialising database to a vanilla state"""
    statusPermissionsInit()
    foldersInit()


def statusInit():
    statusFolders = ("В работе", "Отправлен на утверждение", "Утверждено", "Отклонено")
    parentFolder = excelFolder.objects.get(title="03 - Статусы")
    authorScript = User.objects.get(username="init_script")
    for status in statusFolders:
        newUID = getUID()
        Fold = statusTable(title=status, UID=newUID, author=authorScript, path="prFold", parentFolder=parentFolder)
        createDir("/".join([parentFolder.path, parentFolder.UID, newUID]))
        Fold.save()


def statusPermissionsInit():
    """
        Initialising statuses change permissions
    """
    permissions = []
    content_type_rawmaterials = ContentType.objects.get(app_label="tables", model="rawmaterialstable")
    content_type_subcomponents = ContentType.objects.get(app_label="tables", model="subcomponentstable")

    permissions.append(Permission(codename="set_status_in_work_rawmaterialstable",
                                  name="Can set status 'In work' raw material",
                                  content_type=content_type_rawmaterials))
    permissions.append(Permission(codename="set_status_sent_to_approve_rawmaterialstable",
                                  name="Can set status 'Sent to approve' raw material",
                                  content_type=content_type_rawmaterials))
    permissions.append(Permission(codename="set_status_approved_rawmaterialstable",
                                  name="Can set status 'Approved' raw material",
                                  content_type=content_type_rawmaterials))
    permissions.append(Permission(codename="set_status_declined_rawmaterialstable",
                                  name="Can set status 'Declined' raw material",
                                  content_type=content_type_rawmaterials))
    permissions.append(Permission(codename="set_status_in_work_subcomponentstable",
                                  name="Can set status 'In work' subcomponent",
                                  content_type=content_type_subcomponents))
    permissions.append(Permission(codename="set_status_sent_to_approve_subcomponentstable",
                                  name="Can set status 'Sent to approve' subcomponent",
                                  content_type=content_type_subcomponents))
    permissions.append(Permission(codename="set_status_approved_subcomponentstable",
                                  name="Can set status 'Approved' subcomponent",
                                  content_type=content_type_subcomponents))
    permissions.append(Permission(codename="set_status_declined_subcomponentstable",
                                  name="Can set status 'Declined' subcomponent",
                                  content_type=content_type_subcomponents))
    for permission in permissions:
        permission.save()


def foldersInit():
    authorScript = User(username="init_script", is_staff=True, is_active=True)
    authorScript.save()
    firstFolders = ("prFold", "ghost")
    for fold in firstFolders:
        Fold = excelFolder(title=fold, UID=fold, author=authorScript, path="")
        createDir(fold)
        Fold.save()

    secondFolders = (("01 - Документы", "document"),
                     ("02 - Производство", ""),
                     ("03 - Чертежи и Схемы", ""),
                     ("04 - Персонал", ""),
                     ("05 - Master Data", ""))
    prFold = excelFolder.objects.get(title="prFold")
    for fold in secondFolders:
        newUID = getUID()
        Fold = excelFolder(title=fold[0], UID=newUID, author=authorScript, path="prFold", parentFolder=prFold,
                           tableName=fold[1], )
        createDir("/".join(["prFold", newUID]))
        Fold.save()

    thirdFolders = (
        ("01 - Исходные материалы", "rawMaterial"),
        ("02 - Оборудование", "equipment"),
        ("03 - Субкомпоненты", "subcomponent"),
        ("04 - Готовые изделия", ""))

    productionFold = excelFolder.objects.get(title="02 - Производство")
    for fold in thirdFolders:
        newUID = getUID()
        Fold = excelFolder(title=fold[0], UID=newUID, author=authorScript, path="prFold/" + productionFold.UID,
                           tableName=fold[1], parentFolder=productionFold)
        createDir("/".join([productionFold.path, productionFold.UID, newUID]))
        Fold.save()

    fourthFolders = (
        ("01 - Организации", "organisation"),
        ("02 - Единицы измерения", "measurementUnit"),
        ("03 - Статусы", "status"),
        ("04 - Виды документации", "documentType"),
        ("05 - Подразделение", "department"))

    productionFold = excelFolder.objects.get(title="05 - Master Data")
    for fold in fourthFolders:
        newUID = getUID()
        Fold = excelFolder(title=fold[0], UID=newUID, author=authorScript, path="prFold/" + productionFold.UID,
                           tableName=fold[1], parentFolder=productionFold)
        createDir("/".join([productionFold.path, productionFold.UID, newUID]))
        Fold.save()
    statusInit()
