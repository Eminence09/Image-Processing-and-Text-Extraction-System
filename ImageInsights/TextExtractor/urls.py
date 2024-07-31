from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from TextExtractor import views

urlpatterns = [
    path('', views.file_upload_view, name='file_upload_view'),
    path('result/', views.read_file, name='result'),
    path('<int:line_no>/', views.each_line, name='each_line'),
    # path('display_line/', views.display_line, name='display_line'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)