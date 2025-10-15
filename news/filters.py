import django_filters
from .models import Article

class ArticleFilter(django_filters.FilterSet):
    source = django_filters.CharFilter(field_name="source_domain", lookup_expr="iexact")

    class Meta:
        model = Article
        fields = ["source"]
