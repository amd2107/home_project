from django.db import models


class Traceback(models.Model):
    data = models.TextField()
    is_request = models.BooleanField(default=True)
    trace_id = models.ForeignKey("Traceback", null = True, blank=True, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        verbose_name = 'Traceback'
        verbose_name_plural = 'Tracebacks'
