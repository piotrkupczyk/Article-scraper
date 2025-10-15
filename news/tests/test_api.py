import pytest
from django.urls import reverse
from news.models import Article
from django.utils import timezone

@pytest.mark.django_db
def test_list_endpoint(client):
    Article.objects.create(
        title="Hello",
        html_content="<p>hi</p>",
        text_content="hi",
        source_url="https://example.com/a",
        source_domain="example.com",
        published_at=timezone.now(),
    )
    resp = client.get(reverse("article-list"))
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    assert any(row["title"] == "Hello" for row in data)
