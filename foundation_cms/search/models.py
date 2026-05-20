from django.db import models


class SearchEvent(models.Model):
    query_string = models.CharField(max_length=255, db_index=True)
    language_code = models.CharField(max_length=10, db_index=True)
    results_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["created_at"]),
            models.Index(fields=["query_string", "created_at"]),
            models.Index(fields=["language_code", "created_at"]),
        ]

    def __str__(self):
        return f"{self.query_string} ({self.results_count})"
