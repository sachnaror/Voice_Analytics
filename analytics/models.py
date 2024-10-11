from django.db import models


class AudioFile(models.Model):
    title = models.CharField(max_length=200)
    audio_file = models.FileField(upload_to='audio/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
