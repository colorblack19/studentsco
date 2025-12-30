from django.db import models


class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=2000)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(null=True, blank=True)

    image = models.ImageField(
        upload_to="events/",
        blank=True,
        null=True
    )

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
