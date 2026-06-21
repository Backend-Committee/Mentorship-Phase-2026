"""
URL configuration for inbuddy project.
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('apps.authentication.urls')),
    path('api/users/', include('apps.users.urls')),
    path('api/extractions/', include('apps.text_extraction_engine.urls')),
    path('api/analysis/', include('apps.analysis.urls')),
    path('api/measurements/', include('apps.measurements.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
