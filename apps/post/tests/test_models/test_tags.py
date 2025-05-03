import pytest
from post.models import Tag

@pytest.mark.django_db
class TestTagModel:
    def test_create_tag(self):
        tag = Tag.objects.create(
            name='Test',
            slug='test'
        )
        assert tag.name == 'Test'
        assert tag.slug == 'test'
        assert tag.usage_count == 0

    def test_tag_str(self):
        tag = Tag.objects.create(
            name='Test',
            slug='test'
        )
        assert str(tag) == 'Test'
    
    def test_tag_unique(self):
        Tag.objects.create(name='Test', slug='test')
        with pytest.raises(Exception):
            Tag.objects.create(name='Test', slug='test1')
        with pytest.raises(Exception):
            Tag.objects.create(name='Test1', slug='test')