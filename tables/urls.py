from django.urls import path, include
from tables import views
from tables.models import subcomponentsTable, equipmentTable, rawMaterialsTable
from tables.forms import subcomponentsTableForm,equipmentTableForm, rawMaterialsTableForm
from tables.forms import subcomponentsTableFormUpdate, equipmentTableFormUpdate, rawMaterialsTableFormUpdate
urlpatterns = [
    path('newSubcomponent',views.createTableView.as_view(model = subcomponentsTable, form_class = subcomponentsTableForm), name = 'newSubcomponent'),
    path('newEquipment', views.createTableView.as_view(model = equipmentTable,form_class = equipmentTableForm),name = 'newEquipment'),
    path('newRawMaterial',views.createTableView.as_view(model = rawMaterialsTable,form_class = rawMaterialsTableForm), name = 'newRawMaterial'),
    path('updateSubcomponent/<int:pk>',views.updateTableView.as_view(model = subcomponentsTable, form_class = subcomponentsTableFormUpdate), name = 'updateSubcomponent'),
    path('updateEquipment/<int:pk>', views.updateTableView.as_view(model = equipmentTable, form_class = equipmentTableFormUpdate),name = 'updateEquipment'),
    path('updateRawMaterial/<int:pk>',views.updateTableView.as_view(model = rawMaterialsTable, form_class = rawMaterialsTableFormUpdate), name = 'updateRawMaterial'),
    path('deleteSubcomponent/<int:pk>',
         views.deleteTableView.as_view(model=subcomponentsTable),
         name='deleteSubcomponent'),
    path('deleteEquipment/<int:pk>',
         views.deleteTableView.as_view(model=equipmentTable),
         name='deleteEquipment'),
    path('deleteRawMaterial/<int:pk>',
         views.deleteTableView.as_view(model=rawMaterialsTable),
         name='deleteRawMaterial')
    ,
    ]