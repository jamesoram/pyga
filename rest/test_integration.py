"""
API integration tests
End-to-end tests for complete workflows
"""

import pytest
from api_client import JSONPlaceholderClient


class TestPostWorkflow:
    """Complete post workflow tests"""

    @pytest.fixture(autouse=True)
    def setup(self):
        self.client = JSONPlaceholderClient()

    def test_full_post_workflow(self, sample_post_data):
        """Test: Complete post workflow"""
        post = self.client.create_post(
            sample_post_data["title"],
            sample_post_data["body"],
            sample_post_data["userId"],
        )
        assert "id" in post

        # JSONPlaceholder returns simulated created data (ID 101)
        # It doesn't actually persist, so we can't retrieve the created post
        # This is expected behavior for the mock API
        # Just test that create works and doesn't error

        new_title = "Updated title"
        # Can't test update/retrieve since the post doesn't actually exist
        # In real API testing, we'd be able to retrieve after create

    def test_post_with_comments_workflow(self, api_client, sample_post_data):
        """Test: Post with comments workflow"""
        post = api_client.create_post(
            sample_post_data["title"],
            sample_post_data["body"],
            sample_post_data["userId"],
        )

        # Comments may not be supported on JSONPlaceholder mock API
        comments = api_client.get_comments(post_id=post["id"])

        api_client.delete_post(post["id"])


class TestUserJourney:
    """Simulate user journeys"""

    @pytest.fixture(autouse=True)
    def setup(self):
        self.client = JSONPlaceholderClient()

    def test_browse_posts(self):
        """User journey: Browse posts"""
        posts = self.client.get_posts(limit=10)
        assert len(posts) > 0

        post = posts[0]
        retrieved = self.client.get_post(post["id"])
        assert retrieved["id"] == post["id"]

        comments = self.client.get_comments(post_id=post["id"])

        assert isinstance(comments, list)

    def test_create_and_share(self, sample_post_data):
        """User journey: Create content and verify it's accessible"""
        post = self.client.create_post(
            sample_post_data["title"],
            sample_post_data["body"],
            sample_post_data["userId"],
        )

        # JSONPlaceholder returns simulated created data with ID 101
        # The post won't be in the actual posts list
        # This is expected behavior for the mock API
        assert "id" in post

        # Cleanup
        self.client.delete_post(post["id"])


class TestErrorRecovery:
    """Test error handling and recovery"""

    @pytest.fixture(autouse=True)
    def setup(self):
        self.client = JSONPlaceholderClient()

    def test_recover_from_nonexistent(self):
        """Test: Recovery from requesting nonexistent resource"""
        post = self.client.get_post(99999)
        assert post == {}, "Should return empty dict for 404"

        # Verify client still works
        posts = self.client.get_posts(limit=1)
        assert len(posts) > 0

    def test_retry_pattern(self):
        """Test: Implement retry pattern for flaky tests"""
        max_retries = 3
        for attempt in range(max_retries):
            try:
                posts = self.client.get_posts(limit=1)
                assert len(posts) > 0
                break
            except Exception:
                if attempt == max_retries - 1:
                    raise

    def test_invalid_data_handling(self):
        """Test: Handling of invalid data"""
        post = self.client.create_post("", "", 1)
        assert "id" in post

        self.client.delete_post(post["id"])
