from django.urls import path
from django.views.generic.base import TemplateView
from django.conf import settings
from general import views
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),

    path('prFold/', views.prFold, name = 'prFold'),
    path('prFold/<slug:a_id>/', views.prFold, name='prFold'),
    path('prFold/<slug:a_id>/<slug:b_id>/', views.prFold, name='prFold'),
    path('prFold/<slug:a_id>/<slug:b_id>/<slug:c_id>/', views.prFold, name='prFold'),
    path('prFold/<slug:a_id>/<slug:b_id>/<slug:c_id>/<slug:d_id>/', views.prFold, name='prFold'),
    path('prFold/<slug:a_id>/<slug:b_id>/<slug:c_id>/<slug:d_id>/<slug:f_id>/', views.prFold, name='prFold'),

    path('deleteFolder/<int:pk>/<slug:type>', views.deleteExcel, name='deleteExcel'),
    path('uploadExcelFile', views.uploadExcelFile, name = 'uploadExcelFile'),
    path('newExcelFolder', views.newExcelFolder, name = 'newExcelFolder'),
    path('downloadExcelFile/<int:pk>/', views.downloadExcelFile, name = 'downloadExcelFile'),
    path('renameExcelFile/<int:pk>/', views.renameExcelFile, name='renameExcelFile'),
    path('renameExcelFolder/<int:pk>/', views.renameExcelFolder, name='renameExcelFolder'),
    path('test', views.test, name = 'testUrl'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)