from django.urls import path
from .views import FileUploadView, PDFListView

urlpatterns = [
    path('api/upload/', FileUploadView.as_view(), name='file-upload'),
    path('api/pdfs/', PDFListView.as_view(), name='pdf-list'),
]
