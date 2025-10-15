from rest_framework import serializers
from .models import Article

class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = [
            "id", "title", "html_content", "text_content",
            "source_url", "source_domain", "published_at",
            "created_at", "updated_at"
        ]
