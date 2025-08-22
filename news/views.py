from rest_framework import viewsets, generics
from .models import News
from .serializers import NewsSerializer


class NewsViewSet(viewsets.ModelViewSet):
    queryset = News.objects.all().order_by('-date')
    serializer_class = NewsSerializer
    lookup_field = 'slug'


class NewsDetailBySlugView(generics.RetrieveAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    lookup_field = 'slug'


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


