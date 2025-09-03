from rest_framework import viewsets, generics, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from .models import News
from .serializers import NewsSerializer

class NewsViewSet(viewsets.ModelViewSet):
    queryset = News.objects.all().order_by('order', '-date')
    serializer_class = NewsSerializer
    lookup_field = 'slug'
    parser_classes = (MultiPartParser, FormParser)
    
    @action(detail=True, methods=['patch'])
    def toggle_feature(self, request, slug=None):
        """Toggle the feature status of a news article"""
        news = self.get_object()
        news.feature = not news.feature
        news.save()
        serializer = self.get_serializer(news)
        return Response(serializer.data)

class RelatedNewsBySlugView(generics.ListAPIView):
    serializer_class = NewsSerializer

    def get_queryset(self):
        current_slug = self.kwargs['slug']
        queryset = News.objects.exclude(slug=current_slug).order_by('-date')
        limit_param = self.request.query_params.get('limit')
        if limit_param:
            try:
                limit = int(limit_param)
                if limit > 0:
                    return queryset[:limit]
            except ValueError:
                pass
        return queryset
