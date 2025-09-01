from django.db import models

class Feedback(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"Message from {self.name or 'Anonymous'}"


class FeatureUsage(models.Model):
    feature_name = models.CharField(max_length=100)
    details = models.TextField(blank=True, null=True)
    used_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.feature_name}, {self.details}, {self.used_at}"