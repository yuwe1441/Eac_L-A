from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('lost_found.urls')), # Dito niya tinatawag yung app mo
] 

# Serve uploaded media files even in production.
# Railway provides a writable filesystem at runtime, so this makes uploaded images visible.
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
