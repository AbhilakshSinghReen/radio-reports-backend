from os.path import basename, join
import json

from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, JSONParser
from rest_framework import status

from radio_reports_api.cache import (
    create_folder_in_cache,
    delete_from_cache,
    save_file_to_cache,
)
from radio_reports_api.cloud_storage import (
    upload_to_cloud_storage_from_cache,
)
from radio_reports_api.utils import (
    select_random_segment_names,
)
from radio_reports_api.serializers import (
    ReportSerializer,
)
from radio_reports.settings import CACHE_ROOT
# from radio_reports_api.tasks.nifti_to_segmentation import run_total_segmentator_on_nii_image
# from radio_reports_api.tasks.segmentation_to_mesh import total_segmentator_output_to_objs, segment_names
from radio_reports_api.utils import unique_str
from radio_reports_api.models import Report


class AddReportAPIView(APIView):
    permission_classes = [AllowAny]
    parser_classes = [MultiPartParser]

    def post(self, request):
        admin_secret_header = request.headers.get('X-ABNORMAL_DOCS-ADMIN-SECRET')
        # validate admin secret

        nifti_image_file = request.FILES.get('niftiImage')
        report_data = request.data.get('reportData')
        # validate above 2

        report_media_id = unique_str()
        nii_file_name, nii_file_path = save_file_to_cache(nifti_image_file, report_media_id)

        new_report = Report.objects.create(
            report_media_id=report_media_id,
            meshes_metadata=json.dumps({}),
            original_report=report_data,
            simplified_reports=json.dumps({}),
            processing_status="Initializing..."
        )

        
        
        ts_out_file_path = join(CACHE_ROOT, f"{report_media_id}-segmented.nii.gz")
        meshes_output_dir_path = create_folder_in_cache(report_media_id)

        simplified_reports = {
            'english':  "the simplified report data", # TODO (Dr. Amit): get these from the LLM API
        }
        segments_of_interest = select_random_segment_names(segment_names) # TODO (Dr. Amit): get these from the LLM API

        # Run total segmentor
        run_total_segmentator_on_nii_image(nii_file_path, ts_out_file_path)
        
        # Run convertor to mesh
        meshes_metadata = total_segmentator_output_to_objs(ts_out_file_path, meshes_output_dir_path, segments_of_interest)
        
        # Move meshes to cloud storage
        upload_to_cloud_storage_from_cache(report_media_id, "segment-meshes")

        # Delete nifti from cache
        delete_from_cache(nii_file_name)

        # Delete segmentation from cache
        delete_from_cache(basename(ts_out_file_path))

        new_report = Report.objects.create(
            report_media_id=report_media_id,
            meshes_metadata=json.dumps(meshes_metadata),
            original_report=report_data,
            simplified_reports=json.dumps(simplified_reports),
            processing_status="Processing completed."
        )

        # Generate QR code and return it

        return Response({
            'success': True,
            'result': {
                'reportId': new_report.id,
                'qrCode': "foo",
                'reportLink': "bar",
            },
        }, status=status.HTTP_201_CREATED)

class GetReportAPIView(APIView):
    permission_classes = [AllowAny]
    parser_classes = [JSONParser]

    def post(self, request):
        report_id = request.data.get('reportId')
        # report_passcode = request.data.get('reportPasscode')
        # validate above 1

        try:
            report = Report.objects.get(id=report_id)
            report_serializer = ReportSerializer(report)
        except:
            return Response({
                'success': False,
                'error': {
                    'code': -1,
                    'message': "Invalid reportId"
                },
            }, status=status.HTTP_404_NOT_FOUND)

        return Response({
            'success': True,
            'result': {
                'report': report_serializer.data,
            },
        }, status=status.HTTP_200_OK)
