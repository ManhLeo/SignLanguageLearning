from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib.auth.models import User
from tutorials.models import Tutorial, Category, Difficulty
from accounts.models import UserProfile
from django.db.models import Q
from django.urls import reverse

def is_superuser(user):
    return user.is_superuser

@login_required
@user_passes_test(is_superuser)
def management_main(request):
    """View for the main management dashboard"""
    context = {
        'total_users': User.objects.count(),
        'total_tutorials': Tutorial.objects.count(),
        'total_categories': Category.objects.count(),
    }
    return render(request, 'management/Management_main.html', context)

@login_required
@user_passes_test(is_superuser)
def management_user(request):
    """View for user management"""
    users = User.objects.all().order_by('-date_joined')
    query = request.GET.get('q')
    
    if query:
        users = users.filter(
            Q(username__icontains=query) |
            Q(email__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query)
        )
    
    context = {
        'users': users,
        'query': query
    }
    return render(request, 'management/Management_User.html', context)

@login_required
@user_passes_test(is_superuser)
def toggle_user_status(request, user_id):
    """Toggle user's active status"""
    user = get_object_or_404(User, id=user_id)
    user.is_active = not user.is_active
    user.save()
    messages.success(request, f'User {user.username} status has been updated.')
    return redirect('management:management_user')

@login_required
@user_passes_test(is_superuser)
def management_tutorial(request):
    """View for tutorial management"""
    tutorials = Tutorial.objects.all()
    categories = Category.objects.all()
    query = request.GET.get('q')
    category_id = request.GET.get('category')
    
    if query:
        tutorials = tutorials.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query)
        )
    
    if category_id:
        tutorials = tutorials.filter(category_id=category_id)
    
    # Add tutorial count to each category
    for category in categories:
        category.tutorial_count = Tutorial.objects.filter(category=category).count()
    
    context = {
        'tutorials': tutorials,
        'categories': categories,
        'query': query,
        'selected_category': category_id
    }
    return render(request, 'management/Management_Topic.html', context)

@login_required
@user_passes_test(is_superuser)
def delete_tutorial(request, tutorial_id):
    """Delete a tutorial"""
    tutorial = get_object_or_404(Tutorial, id=tutorial_id)
    tutorial.delete()
    messages.success(request, f'Tutorial "{tutorial.title}" has been deleted.')
    return redirect('management:management_tutorial')

@login_required
@user_passes_test(is_superuser)
def management_category(request):
    """View for category management"""
    categories = Category.objects.all().order_by('name')
    query = request.GET.get('q')
    
    if query:
        categories = categories.filter(name__icontains=query)
    
    context = {
        'categories': categories,
        'query': query
    }
    return render(request, 'management/Management_Category.html', context)

@login_required
@user_passes_test(is_superuser)
def delete_category(request, category_id):
    """Delete a category"""
    category = get_object_or_404(Category, id=category_id)
    category.delete()
    messages.success(request, f'Category "{category.name}" has been deleted.')
    return redirect('management:management_category')

@login_required
@user_passes_test(is_superuser)
def management_word(request, category_id):
    """View for word management within a category"""
    category = get_object_or_404(Category, id=category_id)
    tutorials = Tutorial.objects.filter(category=category)
    
    context = {
        'category': category,
        'tutorials': tutorials,
    }
    return render(request, 'management/Management_Word.html', context)

@login_required
@user_passes_test(is_superuser)
def user_form(request, user_id=None):
    """View for adding or editing user profiles in management"""
    if user_id:
        user = get_object_or_404(User, id=user_id)
        page_title = f'Chỉnh sửa người dùng: {user.username}'
    else:
        user = User()
        page_title = 'Thêm người dùng mới'

    if request.method == 'POST':
        if user_id:
            # Editing existing user
            user.username = request.POST.get('username')
            user.first_name = request.POST.get('first_name')
            user.last_name = request.POST.get('last_name')
            user.email = request.POST.get('email')
            user.is_active = request.POST.get('is_active') == 'true'
            user.save()
            messages.success(request, f'Người dùng {user.username} đã được cập nhật thành công.')
        else:
            # Creating new user
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password') # You might want to add a password field to the form
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')

            # Basic validation: ensure username and password exist
            if not username or not password:
                messages.error(request, 'Tên đăng nhập và mật khẩu không được để trống.')
                # Render the form again with existing data and error
                context = {
                    'user': user, # This will be an empty User object for new user or the existing user for edit
                    'page_title': page_title,
                }
                return render(request, 'management/Management_UserForm.html', context)

            try:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.first_name = first_name
                user.last_name = last_name
                user.is_active = request.POST.get('is_active') == 'true'
                user.save()
                messages.success(request, f'Người dùng {user.username} đã được tạo thành công.')
            except Exception as e:
                messages.error(request, f'Có lỗi xảy ra khi tạo người dùng: {e}')
                # Render the form again with existing data and error
                context = {
                    'user': user, # This will be an empty User object for new user or the existing user for edit
                    'page_title': page_title,
                }
                return render(request, 'management/Management_UserForm.html', context)
        
        return redirect('management:management_user')
    
    context = {
        'user': user,
        'page_title': page_title,
    }
    return render(request, 'management/Management_UserForm.html', context)

@login_required
@user_passes_test(is_superuser)
def topic_form(request, category_id=None):
    """View for adding or editing categories (topics) in management"""
    if category_id:
        category = get_object_or_404(Category, id=category_id)
        page_title = f'Chỉnh sửa chủ đề: {category.name}'
    else:
        category = Category()
        page_title = 'Thêm chủ đề mới'

    if request.method == 'POST':
        if category_id:
            # Editing existing category
            category.name = request.POST.get('name')
            category.description = request.POST.get('description')
            category.save()
            messages.success(request, f'Chủ đề {category.name} đã được cập nhật thành công.')
        else:
            # Creating new category
            name = request.POST.get('name')
            description = request.POST.get('description')

            if not name:
                messages.error(request, 'Tên chủ đề không được để trống.')
                context = {
                    'category': category,
                    'page_title': page_title,
                }
                return render(request, 'management/Management_TopicForm.html', context)
            
            try:
                category = Category.objects.create(name=name, description=description)
                messages.success(request, f'Chủ đề {category.name} đã được tạo thành công.')
            except Exception as e:
                messages.error(request, f'Có lỗi xảy ra khi tạo chủ đề: {e}')
                context = {
                    'category': category,
                    'page_title': page_title,
                }
                return render(request, 'management/Management_TopicForm.html', context)
        
        return redirect('management:management_tutorial') # Redirect back to topic list
    
    context = {
        'category': category,
        'page_title': page_title,
    }
    return render(request, 'management/Management_TopicForm.html', context)

@login_required
@user_passes_test(is_superuser)
def word_form(request, category_id=None, tutorial_id=None):
    """View for adding or editing words (tutorials) in management"""
    current_category_id = None
    if tutorial_id:
        tutorial = get_object_or_404(Tutorial, id=tutorial_id)
        page_title = f'Chỉnh sửa từ vựng: {tutorial.title}'
        current_category_id = tutorial.category.id
    else:
        tutorial = Tutorial()
        if category_id:
            tutorial.category = get_object_or_404(Category, id=category_id)
            page_title = f'Thêm từ vựng mới cho chủ đề: {tutorial.category.name}'
            current_category_id = category_id
        else:
            # This case should ideally not happen if adding from a specific category page
            page_title = 'Thêm từ vựng mới'

    categories = Category.objects.all()
    difficulties = Difficulty.objects.all()

    # Determine cancel URL based on whether a category is known
    if current_category_id:
        cancel_url = reverse('management:management_word', kwargs={'category_id': current_category_id})
    else:
        cancel_url = reverse('management:management_tutorial') # Fallback to general tutorials list

    if request.method == 'POST':
        if tutorial_id:
            # Editing existing tutorial
            tutorial.title = request.POST.get('title')
            tutorial.video_url = request.POST.get('video_url')
            tutorial.category_id = request.POST.get('category')
            tutorial.difficulty_id = request.POST.get('difficulty')
            tutorial.save()
            messages.success(request, f'Từ vựng {tutorial.title} đã được cập nhật thành công.')
        else:
            # Creating new tutorial
            title = request.POST.get('title')
            video_url = request.POST.get('video_url')
            category_id_post = request.POST.get('category') # Use a different variable name to avoid conflict
            difficulty_id_post = request.POST.get('difficulty')

            if not title or not video_url or not category_id_post or not difficulty_id_post:
                messages.error(request, 'Từ vựng, URL Video, chủ đề và mức độ không được để trống.')
                context = {
                    'tutorial': tutorial,
                    'categories': categories,
                    'difficulties': difficulties,
                    'page_title': page_title,
                    'cancel_url': cancel_url,
                    'current_category_id': current_category_id,
                }
                return render(request, 'management/Management_WordForm.html', context)
            
            try:
                tutorial = Tutorial.objects.create(
                    title=title,
                    video_url=video_url,
                    category_id=category_id_post,
                    difficulty_id=difficulty_id_post
                )
                messages.success(request, f'Từ vựng {tutorial.title} đã được tạo thành công.')
            except Exception as e:
                messages.error(request, f'Có lỗi xảy ra khi tạo từ vựng: {e}')
                context = {
                    'tutorial': tutorial,
                    'categories': categories,
                    'difficulties': difficulties,
                    'page_title': page_title,
                    'cancel_url': cancel_url,
                    'current_category_id': current_category_id,
                }
                return render(request, 'management/Management_WordForm.html', context)
        
        # After saving, redirect to the word list for the relevant category
        final_category_id = tutorial.category.id if tutorial.category else current_category_id
        if final_category_id:
            return redirect('management:management_word', category_id=final_category_id)
        else:
            return redirect('management:management_tutorial')
    
    context = {
        'tutorial': tutorial,
        'categories': categories,
        'difficulties': difficulties,
        'page_title': page_title,
        'cancel_url': cancel_url,
        'current_category_id': current_category_id, # Pass for selected category in form
    }
    return render(request, 'management/Management_WordForm.html', context) 