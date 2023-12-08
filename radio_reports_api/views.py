from django.shortcuts import render

from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, JSONParser
from rest_framework import status

from radio_reports_api.cache import (
    save_file_to_cache,
    delete_file_from_cache,
)


class AddReportAPIView(APIView):
    permission_classes = [AllowAny]
    parser_classes = [MultiPartParser]

    def post(self, request):
        admin_secret_header = request.headers.get('X-AD-ADMIN-SECRET')
        print(admin_secret_header)

        # Check if the report has admin secret header

        nifti_image_file = request.FILES.get('niftiImage')
        report_data = request.data.get('reportData')

        save_file_to_cache(nifti_image_file)

        # Generate QR code and return it

        return Response({
            'success': True,
            'result': {
                'qrCode': "foo",
                'reportLink': "bar",
            },
        }, status=status.HTTP_201_CREATED)

class GetReportAPIView(APIView):
    permission_classes = [AllowAny]
    

    def get(self, request):
        pass
