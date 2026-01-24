from django.db import models


class StudentPerformance(models.Model):
    """
    Model to store student performance data.
    Features used for ML prediction.
    """
    hours_studied = models.IntegerField()
    previous_scores = models.IntegerField()
    extracurricular = models.BooleanField()
    sleep_hours = models.IntegerField()
    sample_papers = models.IntegerField()
    performance_index = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Student Performance"
        ordering = ['-created_at']

    def __str__(self):
        return f"Performance Index: {self.performance_index}"
