# backend/config/urls.py

from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView # <--- NEW IMPORT
from django.conf import settings
from django.conf.urls.static import static
from catalog import views as catalog_views 

urlpatterns = [
    # 1. ROOT (Homepage) Redirect: Sends traffic from / to /admin/
    path('', RedirectView.as_view(url='admin/', permanent=False)),
    
    # 2. Main Endpoints
    path('admin/', admin.site.urls),
    path('api/', include('catalog.urls')), 
]

# This is necessary for displaying images (Media files)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# If the API endpoint is needed for manual testing, you can use a separate path for it
# path('api-welcome/', catalog_views.api_root),