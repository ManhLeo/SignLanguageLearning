from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def recognition_home(request):
    return render(request, 'recognition/ai.html') 