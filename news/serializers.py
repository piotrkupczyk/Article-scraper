from rest_framework import serializers
from django.utils.text import Truncator
from django.utils.timezone import localtime
from .models import Article


class ArticleListSerializer(serializers.ModelSerializer):
    published_at_str = serializers.SerializerMethodField()
    text_excerpt = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = [
            "id",
            "title",
            "source_url",
            "source_domain",
            "published_at",
            "published_at_str",
            "text_excerpt",
            "created_at",
            "updated_at",
        ]

    def get_published_at_str(self, obj):
        if not obj.published_at:
            return ""
        return localtime(obj.published_at).strftime("%d.%m.%Y %H:%M:%S")

    def get_text_excerpt(self, obj):
        txt = obj.text_content or ""
        return Truncator(txt).chars(300)


class ArticleDetailSerializer(serializers.ModelSerializer):
    published_at_str = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = [
            "id",
            "title",
            "html_content",
            "text_content",
            "source_url",
            "source_domain",
            "published_at",
            "published_at_str",
            "created_at",
            "updated_at",
            "extraction_note",
        ]

    def get_published_at_str(self, obj):
        if not obj.published_at:
            return ""
        return localtime(obj.published_at).strftime("%d.%m.%Y %H:%M:%S")
