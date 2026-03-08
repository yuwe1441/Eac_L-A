from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('lost_found.urls')), # Dito niya tinatawag yung app mo
]

# Serve uploaded media files in production (Django's static helper only works when DEBUG=True)
# Railway uses a writable filesystem, so this ensures uploaded images can be accessed.
if settings.MEDIA_URL and settings.MEDIA_ROOT:
    urlpatterns += [
        re_path(r'^%s(?P<path>.*)$' % settings.MEDIA_URL.lstrip('/'), serve, {
            'document_root': settings.MEDIA_ROOT,
        }),
    ]
