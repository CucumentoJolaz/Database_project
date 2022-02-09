from general.models import excelFolder
from general.functions.tree_folders import getUID
import os
import boto3


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

    firstFolders = ("prFold", "ghost")
    for fold in firstFolders:
        Fold = excelFolder(title=fold, UID=fold, author="init_script", path="")
        createDir(fold)
        Fold.save()

    secondFolders = ("01 - Документы", "02 - Производство", "03 - Чертежи и Схемы", "04 - Персонал", "05 - Master Data")
    prFold = excelFolder.objects.get(title="prFold")
    for fold in secondFolders:
        newUID = getUID()
        Fold = excelFolder(title=fold, UID=newUID, author="init_script", path="prFold", parentFolder=prFold)
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
        Fold = excelFolder(title=fold[0], UID=newUID, author="init_script", path="prFold/" + productionFold.UID,
                           tableName=fold[1], parentFolder=productionFold)
        createDir("/".join([productionFold.path, productionFold.UID, newUID]))
        Fold.save()

    fourthFolders = (
        ("01 - Организации", "organisation"),
        ("02 - Единицы измерения", "measurementUnit"),
        ("03 - Статусы", "status"),)

    productionFold = excelFolder.objects.get(title="05 - Master Data")
    for fold in fourthFolders:
        newUID = getUID()
        Fold = excelFolder(title=fold[0], UID=newUID, author="init_script", path="prFold/" + productionFold.UID,
                           tableName=fold[1], parentFolder=productionFold)
        createDir("/".join([productionFold.path, productionFold.UID, newUID]))
        Fold.save()
