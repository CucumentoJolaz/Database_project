from django.urls import path
from general import views

urlpatterns = [
    path('', views.home, name='home'),

    path('prFold/', views.prFold, name='prFold'),
    path('prFold/<slug:fold_uid>/', views.prFold, name='prFold_uid'),

    path('deleteFolder/<int:pk>/<slug:type>', views.deleteExcel, name='deleteExcel'),
    path('uploadExcelFile', views.uploadExcelFile, name='uploadExcelFile'),
    path('newExcelFolder', views.newExcelFolder, name='newExcelFolder'),
    path('downloadExcelFile/<int:pk>/', views.downloadExcelFile, name='downloadExcelFile'),
    path('renameExcelFile/<int:pk>/', views.renameExcelFile, name='renameExcelFile'),
    path('renameExcelFolder/<int:pk>/', views.renameExcelFolder, name='renameExcelFolder'),
]

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
