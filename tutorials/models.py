from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Category(models.Model):
    """Model for tutorial categories"""
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"

class Difficulty(models.Model):
    """Model for tutorial difficulty levels"""
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Difficulties"

class Tutorial(models.Model):
    """Model for sign language tutorials"""
    title = models.CharField(max_length=200)
    description = models.TextField()
    video_url = models.URLField()
    thumbnail = models.ImageField(upload_to='tutorials/thumbnails/')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='tutorials')
    difficulty = models.ForeignKey(Difficulty, on_delete=models.CASCADE, related_name='tutorials')
    duration = models.IntegerField(help_text='Duration in minutes')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title

class Exercise(models.Model):
    tutorial = models.ForeignKey(Tutorial, on_delete=models.CASCADE)
    question = models.TextField()
    correct_answer = models.CharField(max_length=200)
    points = models.IntegerField(default=10)
    
    def __str__(self):
        return f"Exercise for {self.tutorial.title}"

class UserExerciseAttempt(models.Model):
    """Model for tracking user exercise attempts"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='exercise_attempts')
    tutorial = models.ForeignKey(Tutorial, on_delete=models.CASCADE, related_name='user_attempts')
    is_correct = models.BooleanField(default=False)
    attempt_time = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.tutorial.title}"

class TutorialProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tutorial = models.ForeignKey(Tutorial, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    progress = models.IntegerField(default=0)  # Progress percentage
    time_spent = models.IntegerField(default=0)  # Time spent in seconds
    points_earned = models.IntegerField(default=0)
    completed_at = models.DateTimeField(null=True, blank=True)
    last_accessed = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'tutorial')
        ordering = ['-last_accessed']

    def __str__(self):
        return f"{self.user.username} - {self.tutorial.title}"

    def save(self, *args, **kwargs):
        if self.completed and not self.completed_at:
            self.completed_at = timezone.now()
        super().save(*args, **kwargs) 