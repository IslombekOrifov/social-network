import pytest
from post.models import PostReport


@pytest.mark.django_db
class TestPostReportModel:
    def test_create_repost(self, sample_post, sample_user):
        report = PostReport.objects.create(
            post=sample_post,
            reporter=sample_user,
            reason='test report'
        )
        assert report.post == sample_post
        assert report.reporter == sample_user
        assert report.reason == 'test report'
        assert not report.is_resolved

    def test_report_unique_together(self, sample_post, sample_user):
        PostReport.objects.create(
            post=sample_post,
            reporter=sample_user,
            reason='test report 1'
        )
        with pytest.raises(Exception):
            PostReport.objects.create(
            post=sample_post,
            reporter=sample_user,
            reason='test report 2'
        )

    def test_report_str(self, sample_post, sample_user):
        report = PostReport.objects.create(
            post=sample_post,
            reporter=sample_user,
            reason='test report'
        )
        assert str(report) == f"Report on post {sample_post.id} by {sample_user.username}"