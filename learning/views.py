from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Avg
from tutorials.models import Tutorial, UserExerciseAttempt
from recognition.models import RecognitionSession
from .models import Assessment, UserProgress

def home(request):
    """Home page view"""
    return render(request, 'index.html')

@login_required
def dashboard(request):
    """User dashboard view"""
    user_progress = UserProgress.objects.filter(user=request.user)
    return render(request, 'learning/dashboard.html', {
        'user_progress': user_progress
    })

@login_required
def progress(request):
    """User progress view"""
    user_progress = UserProgress.objects.filter(user=request.user)
    return render(request, 'learning/progress.html', {
        'user_progress': user_progress
    })

@login_required
def take_assessment(request, assessment_id):
    """View for taking an assessment"""
    assessment = get_object_or_404(Assessment, id=assessment_id)
    return render(request, 'learning/take_assessment.html', {
        'assessment': assessment
    })

@login_required
def submit_assessment(request, assessment_id):
    """View for submitting assessment answers"""
    if request.method == 'POST':
        assessment = get_object_or_404(Assessment, id=assessment_id)
        # Process assessment submission
        messages.success(request, 'Assessment submitted successfully!')
        return redirect('learning:progress')
    return redirect('learning:take_assessment', assessment_id=assessment_id)

@login_required
def progress_data(request):
    # Get user's progress data
    tutorial_progress = Tutorial.objects.annotate(
        attempts=Count('userexerciseattempt', filter=models.Q(
            userexerciseattempt__user=request.user
        )),
        correct_attempts=Count('userexerciseattempt', filter=models.Q(
            userexerciseattempt__user=request.user,
            userexerciseattempt__is_correct=True
        ))
    )
    
    recognition_stats = RecognitionSession.objects.filter(
        user=request.user
    ).aggregate(
        avg_accuracy=Avg('accuracy'),
        total_sessions=Count('id')
    )
    
    context = {
        'tutorial_progress': tutorial_progress,
        'recognition_stats': recognition_stats,
    }
    
    return render(request, 'learning/progress_data.html', context)

@login_required
def main_page(request):
    return render(request, 'learning/main_page.html') 