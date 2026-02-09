from django.db import models
from django.contrib.auth.models import User

class TeacherProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # existing
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # 🔥 NEW (PROFILE FEATURES)
    photo = models.ImageField(
        upload_to="teachers/",
        default="teachers/default.png",
        blank=True
    )
    bio = models.CharField(max_length=100, blank=True)
    online = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
