from django.db import models
from django.contrib.auth.models import User

class ConvertedVideo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="converted_videos")
    video_url = models.URLField()
    converted_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Converted video for {self.user.username} - {self.video_url}"

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Converted Video"
        verbose_name_plural = "Converted Videos"
