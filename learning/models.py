from django.db import models
from django.contrib.auth.models import User
from tutorials.models import Tutorial

class Assessment(models.Model):
    """Model for sign language assessments"""
    title = models.CharField(max_length=200)
    description = models.TextField()
    tutorial = models.ForeignKey(Tutorial, on_delete=models.CASCADE, related_name='assessments')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Question(models.Model):
    """Model for assessment questions"""
    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE, related_name='questions')
    question_text = models.TextField()
    correct_answer = models.CharField(max_length=200)
    points = models.IntegerField(default=1)

    def __str__(self):
        return self.question_text

class UserProgress(models.Model):
    """Model for tracking user learning progress"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='learning_progress')
    tutorial = models.ForeignKey(Tutorial, on_delete=models.CASCADE, related_name='user_progress')
    completed = models.BooleanField(default=False)
    score = models.IntegerField(default=0)
    last_attempt = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'tutorial')

    def __str__(self):
        return f"{self.user.username} - {self.tutorial.title}"

class AssessmentAttempt(models.Model):
    """Model for tracking user assessment attempts"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assessment_attempts')
    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE, related_name='attempts')
    score = models.IntegerField(default=0)
    completed = models.BooleanField(default=False)
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.assessment.title}" 