from rest_framework import generics, filters
from .models import Article
from .serializers import ArticleListSerializer, ArticleDetailSerializer
from .filters import ArticleFilter


class ArticleListView(generics.ListAPIView):
    queryset = Article.objects.all().order_by("-published_at", "-id")
    serializer_class = ArticleListSerializer
    filterset_class = ArticleFilter
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["title", "text_content"] 
    ordering_fields = ["published_at", "created_at", "updated_at"]  


class ArticleDetailView(generics.RetrieveAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleDetailSerializer
