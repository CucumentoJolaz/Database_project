from django.urls import path
from tables.views import createProcessingView, updateProcessingView, deleteProcessingView


urlpatterns = [
    path('new/<slug:tableType>', createProcessingView, name='newInstance'),
    path('update/<slug:tableType>/<slug:UID>', updateProcessingView, name='updateInstance'),
    path('delete/<slug:tableType>/<slug:UID>', deleteProcessingView, name='deleteInstance')
    # (model=subcomponentsTable, form_class=subcomponentsTableForm),
    #path('newEquipment', views.createTableView.as_view(model=subcomponentsTable, form_class=subcomponentsTableForm),
    #     name='newEquipment'),
    # path('newEquipment', views.createTableView.as_view(model=equipmentTable, form_class=equipmentTableForm),
    #      name='newEquipment'),
    # path('newRawMaterial', views.createTableView.as_view(model=rawMaterialsTable, form_class=rawMaterialsTableForm),
    #      name='newRawMaterial'),
    # path('updateSubcomponent/<slug:UID>',
    #      views.updateTableView.as_view(model=subcomponentsTable, form_class=subcomponentsTableFormUpdate),
    #      name='updateSubcomponent'),
    # path('updateEquipment/<slug:UID>',
    #      views.updateTableView.as_view(model=equipmentTable, form_class=equipmentTableFormUpdate),
    #      name='updateEquipment'),
    # path('updateRawMaterial/<slug:UID>',
    #      views.updateTableView.as_view(model=rawMaterialsTable, form_class=rawMaterialsTableFormUpdate),
    #      name='updateRawMaterial'),
    # path('deleteSubcomponent/<int:pk>',
    #      views.deleteTableView.as_view(model=subcomponentsTable),
    #      name='deleteSubcomponent'),
    # path('deleteEquipment/<int:pk>',
    #      views.deleteTableView.as_view(model=equipmentTable),
    #      name='deleteEquipment'),
    # path('deleteRawMaterial/<int:pk>',
    #      views.deleteTableView.as_view(model=rawMaterialsTable),
    #      name='deleteRawMaterial'),
    # path('approve/<slug:tableType>/<int:pk>',
    #      # views.approveTable,
    #      # name='approveTable')
    ,
]
