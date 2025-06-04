from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def recognition_home(request):
    return render(request, 'recognition/home.html')

@login_required
def practice_recognition(request):
    return render(request, 'recognition/practice.html')

@login_required
def recognition_result(request):
    return render(request, 'recognition/result.html') 