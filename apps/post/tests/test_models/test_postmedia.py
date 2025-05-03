import pytest
from post.models import PostMedia

@pytest.mark.django_db
class TestPostMedia:
    def test_create_image_media(self,sample_post, sample_image):
        media = PostMedia.objects.create(
            post=sample_post,
            file=sample_image,
            is_video=False
        )
        assert 'test.jpg' in media.file.name
        assert not media.is_video
        assert media.width == 100
        assert media.height == 100

    def test_create_video_media(self, sample_post, sample_video):
        media = PostMedia.objects.create(
            post=sample_post,
            file=sample_video,
            is_video=True,
            duration=120.5
        )
        assert 'test.mp4' in media.file.name
        assert media.is_video
        assert media.duration == 120.5

    def test_media_ordering(self, sample_post, sample_image):
        media1 = PostMedia.objects.create(
            post=sample_post,
            file=sample_image,
            order=2
        )
        media2 = PostMedia.objects.create(
            post=sample_post,
            file=sample_image,
            order=1
        )
        media = sample_post.media_files.all()
        assert media[0] == media2
        assert media[1] == media1

    def test_media_str(self, sample_post, sample_image):
        media = PostMedia.objects.create(
            post=sample_post,
            file=sample_image
        )
        assert str(media) == f"Media for post {sample_post.id}"