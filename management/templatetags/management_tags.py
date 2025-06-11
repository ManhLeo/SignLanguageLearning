from django import template
from django.contrib.auth.models import User
from tutorials.models import Tutorial, Category

register = template.Library()

@register.simple_tag
def get_total_users():
    """Get total number of users"""
    return User.objects.count()

@register.simple_tag
def get_total_tutorials():
    """Get total number of tutorials"""
    return Tutorial.objects.count()

@register.simple_tag
def get_total_categories():
    """Get total number of categories"""
    return Category.objects.count()

@register.filter
def get_user_status(user):
    """Get user status badge class"""
    return 'active' if user.is_active else 'inactive'

@register.filter
def get_tutorial_count(category):
    """Get number of tutorials in a category"""
    return Tutorial.objects.filter(category=category).count()

@register.filter
def get_category_name(tutorial):
    """Get category name for a tutorial"""
    return tutorial.category.name if tutorial.category else 'Uncategorized' 