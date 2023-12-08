from django.db import models


class Report(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    report_id = models.CharField(max_length=255)
    meshes_metadata = models.TextField()
    simplified_reports = models.TextField()
    processing_status = models.TextField()
