from django.db import models
from django.contrib.auth.models import User

class Sign(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='sign_images/')
    video_demonstration = models.FileField(upload_to='sign_videos/')
    
    def __str__(self):
        return self.name

class RecognitionAttempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    sign = models.ForeignKey(Sign, on_delete=models.CASCADE)
    video_attempt = models.FileField(upload_to='user_attempts/')
    confidence_score = models.FloatField()
    is_correct = models.BooleanField(default=False)
    feedback = models.TextField(blank=True)
    attempted_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username}'s attempt for {self.sign.name}"

class RecognitionSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    total_attempts = models.IntegerField(default=0)
    correct_attempts = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.user.username}'s session at {self.start_time}"
    
    @property
    def accuracy(self):
        if self.total_attempts == 0:
            return 0
        return (self.correct_attempts / self.total_attempts) * 100 