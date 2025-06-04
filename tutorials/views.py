from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Tutorial, Category, Difficulty

def tutorial_list(request):
    """View for listing all tutorials"""
    tutorials = Tutorial.objects.all()
    categories = Category.objects.all()
    difficulties = Difficulty.objects.all()
    
    return render(request, 'tutorials/tutorial_list.html', {
        'tutorials': tutorials,
        'categories': categories,
        'difficulties': difficulties,
    })

def tutorial_detail(request, tutorial_id):
    """View for displaying tutorial details"""
    tutorial = get_object_or_404(Tutorial, id=tutorial_id)
    related_tutorials = Tutorial.objects.filter(
        category=tutorial.category
    ).exclude(id=tutorial_id)[:3]
    
    return render(request, 'tutorials/tutorial_detail.html', {
        'tutorial': tutorial,
        'related_tutorials': related_tutorials,
    })

def tutorials_by_category(request, category):
    """View for filtering tutorials by category"""
    tutorials = Tutorial.objects.filter(category__name=category)
    return render(request, 'tutorials/tutorials_by_category.html', {
        'tutorials': tutorials,
        'category': category,
    })

def tutorials_by_difficulty(request, difficulty):
    """View for filtering tutorials by difficulty"""
    tutorials = Tutorial.objects.filter(difficulty__name=difficulty)
    return render(request, 'tutorials/tutorials_by_difficulty.html', {
        'tutorials': tutorials,
        'difficulty': difficulty,
    })

def tutorial_search(request):
    """View for searching tutorials"""
    query = request.GET.get('q', '')
    if query:
        tutorials = Tutorial.objects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query)
        )
    else:
        tutorials = Tutorial.objects.none()
    
    return render(request, 'tutorials/tutorial_search.html', {
        'tutorials': tutorials,
        'query': query,
    }) 