import tables.functions.table_check as tc
import general.functions.tree_folders as genFunc


class tablesLinkTreeGenerator(genFunc.LinkTreeGenerator):

    def __init__(self, tableType: str):
        tableInfoProc = tc.tableInfoProcessor()
        self.tableModel = tableInfoProc.tableTypeModel(tableType)

    def getLinksUIDsTreeTable(self, tableUID):
        """Return list of tuples with names and links
        for folders generator. Supposed to be included to updateTableTeplate template"""
        firstFolder = self.tableModel.objects.get(UID=tableUID)
        otherFoldersTree = self.getFolderTree(folderUID=firstFolder.parentFolder.UID)
        linksUIDsTree = self.generateLinksUIDsTree(otherFoldersTree)
        return linksUIDsTree