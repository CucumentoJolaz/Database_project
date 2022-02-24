from django.urls import path
from tables.views import createProcessingView, updateProcessingView, deleteProcessingView, changeStatusView


urlpatterns = [
    path('new/<slug:tableType>', createProcessingView, name='newInstance'),
    path('update/<slug:tableType>/<slug:UID>', updateProcessingView, name='updateInstance'),
    path('delete/<slug:tableType>/<slug:UID>', deleteProcessingView, name='deleteInstance'),
    path('changeStatus/<slug:tableType>/<slug:UID>', changeStatusView, name='changeStatus')
]
