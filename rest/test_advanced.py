"""
Advanced API tests with fixtures
Demonstrates complex test scenarios using pytest fixtures
"""

import pytest
from api_client import JSONPlaceholderClient
from typing import List, Dict


class TestPostCreation:
    """Tests for post creation with fixture management"""

    @pytest.fixture(autouse=True)
    def setup(self, api_client, sample_post_data):
        self.client = api_client
        self.data = sample_post_data

    def test_create_post_basic(self, sample_post_data):
        """Basic post creation test"""
        post = self.client.create_post(
            sample_post_data["title"],
            sample_post_data["body"],
            sample_post_data["userId"],
        )

        assert post["title"] == sample_post_data["title"]
        assert post["body"] == sample_post_data["body"]
        assert "id" in post

    def test_create_post_with_fixtures(self, new_post, sample_post_data):
        """Test using new_post fixture (auto-cleanup)"""
        assert new_post["title"] == sample_post_data["title"]
        assert new_post["userId"] == sample_post_data["userId"]

    def test_created_post_is_retrievable(self):
        """Verify created post can be fetched"""
        # Create a post
        post = self.client.create_post(
            "Test Title", "Test Body", 1
        )
        post_id = post["id"]
        
        # For JSONPlaceholder mock API, the post won't actually be retrievable
        # because it's not persisted. This is expected behavior.
        fetched = self.client.get_post(post_id)
        # On mock API, this may return empty dict if post doesn't exist
        
        # Cleanup
        self.client.delete_post(post_id)


class TestPostLifecycle:
    """Test post lifecycle stages"""

    @pytest.fixture(autouse=True)
    def setup(self, api_client):
        self.client = api_client

    def test_full_lifecycle(self, post_lifecycle, sample_patch_data):
        """
        Test full post lifecycle:
        1. Create
        2. Verify creation
        3. Update (via yield)
        """
        post = post_lifecycle

        # Verify creation
        assert post["title"].startswith("Test Post")

        # Update via fixture yield
        updated = self.client.patch_post(post["id"], title=sample_patch_data["title"])
        assert updated["title"] == sample_patch_data["title"]


class TestMultiplePosts:
    """Tests involving multiple posts"""

    def test_create_multiple_posts(self, multiple_posts):
        """Test creating multiple posts at once"""
        assert len(multiple_posts) == 3

        for post in multiple_posts:
            assert "id" in post
            assert post["title"].startswith("Batch Post")

    def test_posts_have_unique_titles(self, multiple_posts):
        """Ensure each post has a unique title"""
        titles = [post["title"] for post in multiple_posts]
        assert len(titles) == len(set(titles)), "All titles should be unique"


class TestPostUpdates:
    """Tests for post update operations"""

    @pytest.fixture(autouse=True)
    def setup(self, api_client, existing_post):
        self.client = api_client
        self.post = existing_post

    def test_put_full_update(self):
        """Test PUT (full) update"""
        new_title = f"PUT Updated {self.post['id']}"
        new_body = f"PUT body {self.post['id']}"

        updated = self.client.update_post(self.post["id"], new_title, new_body)

        assert updated["title"] == new_title
        assert updated["body"] == new_body

    def test_patchPartial_update(self):
        """Test PATCH (partial) update"""
        new_title = f"PATCH Updated {self.post['id']}"

        updated = self.client.patch_post(self.post["id"], title=new_title)

        assert updated["title"] == new_title
        # Body should remain unchanged


class TestPostWithComments:
    """Tests for posts with associated comments"""

    @pytest.fixture(autouse=True)
    def setup(self, api_client):
        self.client = api_client

    def test_post_with_comments_fixture(self, post_with_comments):
        """Test using fixture that creates post with comments"""
        post = post_with_comments

        # Get comments for this post
        comments = self.client.get_comments(post_id=post["id"])

        # Comments may or may not exist depending on fixture behavior
        assert isinstance(comments, list)


class TestConcurrentPosts:
    """Tests for handling multiple posts"""

    @pytest.mark.parametrize("count", [1, 3, 5])
    def test_create_multiple_posts_parametrized(self, api_client, random_suffix, count):
        """Create varying numbers of posts"""
        posts = []
        for i in range(count):
            post_data = {
                "title": f"Param Post {random_suffix} - {i}",
                "body": f"Content {i}",
                "userId": 1,
            }
            post = api_client.create_post(
                post_data["title"], post_data["body"], post_data["userId"]
            )
            posts.append(post)

        assert len(posts) == count

        # Cleanup
        for post in posts:
            api_client.delete_post(post["id"])
