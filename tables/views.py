from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from tables.functions.views.change_status import processChangeStatusView
from tables.functions.views.create import processCreateView, initialiseCreateView
from tables.functions.views.delete import processDeleteView, FALSE_DELETION
from tables.functions.views.update import initialiseUpdateView, processUpdateView


@login_required
def createProcessingView(request, **kwargs):
    """
    Creating new table instance.
    createProcessingView(request, **kwargs) -> redirect() | render():
    """
    try:
        if request.method == 'POST':
            processCreateView(request, **kwargs)
            return redirect(f"/{request.POST['pathBack']}")

        if request.method == 'GET':
            renderDict = initialiseCreateView(request, **kwargs)
            return render(request, 'tables/createTable.html', renderDict)
    except KeyError:
        return redirect('home')


@login_required
def updateProcessingView(request, **kwargs):
    """
    Updating table instance.
    updateProcessingView(request, **kwargs) -> redirect() | render():
    """
    if request.method == 'POST':
        if processUpdateView(request, **kwargs):
            updateMessage = "Компонент успешно обновлён!"
        else:
            updateMessage = "Не получилось обновить компонент."

        return redirect(f"/{request.POST['pathToInstance']}?updateMessage={updateMessage}")

    if request.method == 'GET':
        renderDict = initialiseUpdateView(request, **kwargs)
        return render(request, 'tables/updateTable.html', renderDict)


@login_required
def deleteProcessingView(request, **kwargs):
    """
    Deleting table instance
    deleteProcessingView(request, **kwargs) -> redirect():
    """
    if request.method == 'POST':
        processDeleteView(deletionType=FALSE_DELETION, **kwargs)
        return redirect(request.POST['pathToParentFolder'])
    else:
        return redirect('home')


@login_required
def changeStatusView(request, **kwargs):
    """
    Changing status of the table instance;
    changeStatusView(request, **kwargs) -> redirect():
    """
    if request.method == "POST":
        if processChangeStatusView(request, **kwargs):
            updateMessage = "Статус успешно изменён"
        else:
            updateMessage = "У вас нет прав для изменения статуса на данный"
        return redirect(f"/{request.POST['pathToInstance']}?updateMessage={updateMessage}")
    else:
        return redirect('home')

