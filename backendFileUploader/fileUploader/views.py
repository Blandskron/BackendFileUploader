from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
import os

class FileUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        file = request.FILES.get('file')
        if not file:
            return Response({'status': 'failed', 'message': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)

        # Guarda el archivo usando default_storage
        path = default_storage.save(file.name, ContentFile(file.read()))
        
        # Opcional: Obtiene la URL del archivo
        file_url = default_storage.url(path)

        return Response({'status': 'success', 'file_name': file.name, 'file_url': file_url}, status=status.HTTP_201_CREATED)

class PDFListView(APIView):
    def get(self, request, *args, **kwargs):
        files_dir = os.path.join(settings.MEDIA_ROOT)

        try:
            file_list = [
                {'name': file_name, 'url': request.build_absolute_uri(settings.MEDIA_URL + file_name)}
                for file_name in os.listdir(files_dir)
                if file_name.endswith('.pdf')
            ]
            return Response(file_list, status=status.HTTP_200_OK)
        except FileNotFoundError:
            return Response({'status': 'failed', 'message': 'No files found'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, *args, **kwargs):
        file_name = request.query_params.get('name')
        if not file_name:
            return Response({'status': 'failed', 'message': 'File name not provided'}, status=status.HTTP_400_BAD_REQUEST)

        file_path = os.path.join(settings.MEDIA_ROOT, file_name)
        if os.path.exists(file_path):
            os.remove(file_path)
            return Response({'status': 'success', 'message': 'File deleted'}, status=status.HTTP_200_OK)
        else:
            return Response({'status': 'failed', 'message': 'File not found'}, status=status.HTTP_404_NOT_FOUND)