import django_filters
from .models import Article

class ArticleFilter(django_filters.FilterSet):
    source = django_filters.CharFilter(method="filter_source")

    class Meta:
        model = Article
        fields = ["source"]

    def filter_source(self, queryset, name, value):
        if value is None:
            return queryset
        value = value.strip()
        if not value:
            return queryset
        return queryset.filter(source_domain__iexact=value)
