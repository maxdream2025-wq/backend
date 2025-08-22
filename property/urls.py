from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('api/', include('propertyCrud.urls')),
    path('api/v1/', include('news.urls')),
    path('api/v1/', include('testimonial.urls')),
    path('api/v1/', include('inquiry.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)