from django.shortcuts import redirect
from django.urls import reverse

class SuperuserRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        # Check if user is superuser and just logged in
        if request.user.is_authenticated and request.user.is_superuser:
            # Check if the current path is the main page
            if request.path == reverse('learning:main_page'):
                return redirect('management:management_main')
        
        return response 