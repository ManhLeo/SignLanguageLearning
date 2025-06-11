from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('learning.urls', namespace='learning')),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('tutorials/', include('tutorials.urls', namespace='tutorials')),
    path('recognition/', include('recognition.urls', namespace='recognition')),
    path('management/', include('management.urls', namespace='management')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 