from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden
from .forms import UserRegistrationForm, UserProfileForm, UserUpdateForm, CustomPasswordChangeForm
from .models import UserProfile, LearningProgress
from tutorials.models import Tutorial
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect

def is_superuser(user):
    return user.is_superuser

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log the user in after registration
            messages.success(request, f'Account created for {user.username}!')
            # Redirect superusers to management dashboard, others to main page
            if user.is_superuser:
                return redirect('management:management_main')
            return redirect('learning:main_page')
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/sign_up.html', {'form': form})

@login_required
def profile(request):
    user_profile = request.user.userprofile
    learning_progress = LearningProgress.objects.filter(user=request.user)
    completed_tutorials = Tutorial.objects.filter(
        learningprogress__user=request.user,
        learningprogress__completed=True
    )
    
    context = {
        'user_profile': user_profile,
        'learning_progress': learning_progress,
        'completed_tutorials': completed_tutorials,
    }
    return render(request, 'accounts/profile.html', context)

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user.userprofile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('accounts:profile')
    else:
        form = UserProfileForm(instance=request.user.userprofile)
    return render(request, 'accounts/edit_profile.html', {'form': form})

@login_required
def change_password(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password has been updated!')
            return redirect('accounts:profile')
    else:
        form = CustomPasswordChangeForm(request.user)
    return render(request, 'accounts/change_password.html', {'form': form})

# Superuser management views
@login_required
@user_passes_test(is_superuser)
def user_list(request):
    users = User.objects.all().select_related('userprofile')
    return render(request, 'accounts/user_list.html', {'users': users})

@login_required
@user_passes_test(is_superuser)
def user_detail(request, user_id):
    user = get_object_or_404(User, id=user_id)
    # Prevent superusers from viewing other superusers' details
    if user.is_superuser and request.user != user:
        messages.error(request, "You cannot view the details of another superuser.")
        return redirect('accounts:user_list')

    user_profile, created = UserProfile.objects.get_or_create(user=user)
    learning_progress = LearningProgress.objects.filter(user=user)
    completed_tutorials = Tutorial.objects.filter(
        learningprogress__user=user,
        learningprogress__completed=True
    )
    
    context = {
        'target_user': user,
        'user_profile': user_profile,
        'learning_progress': learning_progress,
        'completed_tutorials': completed_tutorials,
    }
    return render(request, 'accounts/user_detail.html', context)

@login_required
@user_passes_test(is_superuser)
def user_edit(request, user_id):
    user = get_object_or_404(User, id=user_id)
    # Prevent superusers from editing other superusers
    if user.is_superuser and request.user != user:
        messages.error(request, "You cannot edit another superuser's profile.")
        return redirect('accounts:user_list')

    user_profile, created = UserProfile.objects.get_or_create(user=user)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            messages.success(request, f'Profile for {user.username} has been updated!')
            return redirect('accounts:user_detail', user_id=user.id)
    else:
        form = UserProfileForm(instance=user_profile)
    return render(request, 'accounts/user_edit.html', {'form': form, 'target_user': user})

@login_required
@user_passes_test(is_superuser)
def user_delete(request, user_id):
    user = get_object_or_404(User, id=user_id)
    # Prevent superusers from deleting other superusers
    if user.is_superuser and request.user != user:
        messages.error(request, "You cannot delete another superuser.")
        return redirect('accounts:user_list')
        
    if request.method == 'POST':
        username = user.username
        user.delete()
        messages.success(request, f'User {username} has been deleted.')
        return redirect('accounts:user_list')
    return render(request, 'accounts/user_confirm_delete.html', {'target_user': user}) 
def custom_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data.get('username'),
                password=form.cleaned_data.get('password')
            )
            if user is not None:
                login(request, user)
                if user.is_superuser:
                    return redirect('management:management_main')
                return redirect('learning:main_page')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})