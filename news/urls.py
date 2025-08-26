from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import NewsViewSet, RelatedNewsBySlugView

router = DefaultRouter()
router.register(r'news', NewsViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('news/<slug:slug>/related/', RelatedNewsBySlugView.as_view(), name='related-news'),
]
