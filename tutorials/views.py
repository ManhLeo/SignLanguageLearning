from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Tutorial, Category, Difficulty
import re # Import the regular expression module

def tutorial_list(request):
    """View for listing all tutorials (topics) and related data"""
    # Fetch all categories (topics)
    topics = Category.objects.all()
    
    # You might want to add annotations here to calculate lessons_count and progress for each topic
    # from related Tutorial objects if needed for the template.
    
    # Original lines (tutorials and difficulties might still be needed for other parts of the template)
    tutorials = Tutorial.objects.all() # Keep if needed elsewhere in topic.html
    difficulties = Difficulty.objects.all() # Keep if needed elsewhere in topic.html

    return render(request, 'tutorials/topic.html', {
        'topics': topics, # Pass categories as 'topics'
        'tutorials': tutorials,
        'categories': Category.objects.all(), # Keep if needed elsewhere in topic.html
        'difficulties': difficulties,
    })

def tutorial_detail(request, tutorial_id):
    """View for displaying tutorial details (individual vocabulary item) """
    tutorial = get_object_or_404(Tutorial, id=tutorial_id)
    related_tutorials = Tutorial.objects.filter(
        category=tutorial.category
    ).exclude(id=tutorial_id)[:3]
    
    return render(request, 'tutorials/tutorial_detail.html', {
        'tutorial': tutorial,
        'related_tutorials': related_tutorials,
    })

def tutorials_by_category(request, category_name):
    """View for filtering tutorials by category name"""
    category = get_object_or_404(Category, name=category_name)
    tutorials = Tutorial.objects.filter(category=category)
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

# View for displaying vocabulary for a specific topic
def vocabulary_detail(request, topic_id):
    """View for displaying vocabulary for a specific topic"""
    # 1. Get the Category object (topic)
    topic = get_object_or_404(Category, id=topic_id)
    
    # 2. Query Tutorial objects (vocabulary) related to this category
    vocabulary_list = Tutorial.objects.filter(category=topic)
    
    # 3. Render vocabulary.html template with topic and vocabulary_list
    return render(request, 'tutorials/vocabulary.html', {
        'topic': topic,
        'vocabulary_list': vocabulary_list,
        'topics': Category.objects.all(), # Pass all categories as 'topics'
        'current_topic_id': topic_id, # Pass current topic ID for highlighting
    })

# View for the practice home page
def practice_home(request):
    """View for the practice home page"""
    # Fetch all categories (topics) for practice
    topics = Category.objects.all()
    
    # Render the user-provided practice.html template with topics
    return render(request, 'tutorials/practice.html', {'topics': topics})

# View for practice detail for a specific topic
def practice_detail(request, topic_id):
    """View for practice detail for a specific topic"""
    print(f"Entering practice_detail view for topic_id: {topic_id}")
    # Get the Category object (topic)
    topic = get_object_or_404(Category, id=topic_id)
    
    # Fetch Tutorial objects (vocabulary) related to this topic
    vocabulary_list = Tutorial.objects.filter(category=topic)
    
    # TODO: Add logic here to fetch practice data (exercises, etc.) related to the topic
    
    # Render the correct template practice_detail.html
    return render(request, 'tutorials/practice_detail.html', {
        'topic': topic,
        'vocabulary_list': vocabulary_list # Pass the list of vocabulary
    })

def vocabulary(request):
    """View for vocabulary page"""
    # Get all categories
    categories = Category.objects.all()
    print(f"Number of categories fetched: {categories.count()}") # Add this line to check the count
    
    # Get selected category from request
    selected_category_id = request.GET.get('category')
    selected_category = None
    tutorials = []
    
    if selected_category_id:
        selected_category = get_object_or_404(Category, id=selected_category_id)
        tutorials = Tutorial.objects.filter(category=selected_category)
    
    return render(request, 'tutorials/vocabulary.html', {
        'categories': categories,
        'selected_category': selected_category,
        'tutorials': tutorials
    })

def vd_vocabulary(request, tutorial_id):
    """View for vocabulary detail"""
    # Get the current Tutorial object
    tutorial = get_object_or_404(Tutorial, id=tutorial_id)

    # Get all tutorials in the same category, ordered by updated date
    category_tutorials = Tutorial.objects.filter(
        category=tutorial.category
    ).order_by('updated_at') # Changed from created_at to updated_at

    # Find the index of the current tutorial in the ordered list
    current_tutorial_index = list(category_tutorials).index(tutorial)

    # Determine the next tutorial
    next_tutorial = None
    if current_tutorial_index < len(category_tutorials) - 1:
        next_tutorial = category_tutorials[current_tutorial_index + 1]

    video_id = None
    video_id_match = None
    if tutorial.video_url:
        print(f"Original video_url from DB: {tutorial.video_url}") # Added print
        # Remove the leading '@' and extract the video ID from YouTube URL
        youtube_url = tutorial.video_url[1:] # Slice from index 1 to remove '@'
        # Use regex to extract video ID from various YouTube URL formats
        video_id_match = re.search(r'(?:v=|/)([0-9A-Za-z_-]{11}).*', youtube_url)
        if video_id_match:
            video_id = video_id_match.group(1)
    
    print(f"Generated video_id: {video_id}") # Added print
    
    # Render the vocabulary detail template
    return render(request, 'tutorials/vd_vocabulary.html', {
        'tutorial': tutorial,
        'video_id': video_id if video_id_match else None, # Pass the video ID
        'next_tutorial_id': next_tutorial.id if next_tutorial else None
    })

# View for the exam page
def exam_page(request):
    """View for the exam page"""
    # TODO: Add logic here to fetch exam questions, options, etc.
    return render(request, 'tutorials/exam_page.html', {}) 