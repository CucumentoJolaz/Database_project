from django.core.exceptions import PermissionDenied

from tables.models import statusTable


def checkStatusPermissions(request, statusObj) -> bool:
    """
    Checking if user has permission to change statuses of the element
    checkStatusPermissions(request, status_id) -> bool
    """
    approvedStatus = statusTable.objects.get(title="Утверждено")
    declinedStatus = statusTable.objects.get(title="Отклонено")

    if statusObj == approvedStatus:
        if (request.user.has_perm('set_status_approved_rawmaterialstable') or \
                request.user.has_perm('set_status_approved_subcomponentstable')):
            return True
        else:
            raise PermissionDenied()
    elif statusObj == declinedStatus:
        if (request.user.has_perm('set_status_declined_rawmaterialstable') or \
                request.user.has_perm('set_status_declined_subcomponentstable')):
            return True
        else:
            raise PermissionDenied()
    else:
        return True


def checkIfCanUpdate(request, statusObj=None) -> bool:
    """
    Checking if user has permission to change an object
    checkIfCanUpdate(request, status_id) -> bool
    """
    if statusObj:
        return checkStatusPermissions(request, statusObj)
    elif request.user.is_staff == True:
        return True
    else:
        return False
