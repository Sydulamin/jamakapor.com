from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('secret_superadmin/', admin.site.urls),
    path('', include('home.urls')),
<<<<<<< HEAD
    path('authentication_backend/', include('authentication_backend.urls')),
    
    path('accounts/', include('allauth.urls')),
<<<<<<< HEAD
=======
>>>>>>> 8ac853f... Templates config
=======

>>>>>>> 1a2fe74802877d6e0e28ce48b891b158fc9cbf42
]

# Serve static and media files in development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)