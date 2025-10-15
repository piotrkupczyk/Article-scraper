from rest_framework import generics
from .models import Article
from .serializers import ArticleSerializer
from .filters import ArticleFilter

class ArticleListView(generics.ListAPIView):
    queryset = Article.objects.all().order_by("-published_at", "-id")
    serializer_class = ArticleSerializer
    filterset_class = ArticleFilter

class ArticleDetailView(generics.RetrieveAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
