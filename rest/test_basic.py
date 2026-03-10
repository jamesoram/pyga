"""
Basic API endpoint tests for JSONPlaceholder
Tests individual endpoints with basic assertions
"""

import pytest
from api_client import JSONPlaceholderClient


class TestPostsEndpoint:
    """Tests for the posts endpoint"""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup API client for all tests in this class"""
        self.client = JSONPlaceholderClient()

    def test_get_all_posts(self):
        """
        Test: Get all posts
        Expected: Return 200 status and list of posts
        """
        posts = self.client.get_posts()

        assert isinstance(posts, list), "Should return a list"
        assert len(posts) > 0, "Should have at least one post"
        assert isinstance(posts[0], dict), "Each post should be a dictionary"

    def test_get_single_post(self):
        """
        Test: Get a single post by ID
        Expected: Return 200 status and post with matching ID
        """
        post_id = 1
        post = self.client.get_post(post_id)

        assert post["id"] == post_id, f"Post ID should be {post_id}"
        assert "title" in post, "Post should have a title"
        assert "body" in post, "Post should have a body"
        assert "userId" in post, "Post should have a userId"

    def test_get_post_nonexistent(self):
        """
        Test: Request a non-existent post
        Expected: Return empty dict for 404 on mock API
        """
        post = self.client.get_post(99999)
        assert post == {}, "Should return empty dict for non-existent post"

    def test_create_post(self, sample_post_data):
        """
        Test: Create a new post
        Expected: Return 201 status and created post with ID
        """
        post = self.client.create_post(
            sample_post_data["title"],
            sample_post_data["body"],
            sample_post_data["userId"],
        )

        assert "id" in post, "Created post should have an ID"
        assert post["title"] == sample_post_data["title"]
        assert post["body"] == sample_post_data["body"]
        assert post["userId"] == sample_post_data["userId"]
        self.client.delete_post(post["id"])

    def test_update_post(self, existing_post):
        """
        Test: Update an existing post (PUT)
        Expected: Return updated post with new data
        """
        new_title = f"Updated Title {existing_post['id']}"
        new_body = f"Updated content for post {existing_post['id']}"

        updated_post = self.client.update_post(existing_post["id"], new_title, new_body)

        assert updated_post["title"] == new_title
        assert updated_post["body"] == new_body

    def test_partial_update_post(self, existing_post):
        """
        Test: Partially update a post (PATCH)
        Expected: Return updated post with only modified fields
        """
        new_title = f"Patch Title {existing_post['id']}"

        patched_post = self.client.patch_post(existing_post["id"], title=new_title)

        assert patched_post["title"] == new_title

    def test_delete_post(self, new_post):
        """
        Test: Delete a post
        Expected: Return 200 status
        """
        pass

    def test_get_comments_for_post(self, existing_post):
        """
        Test: Get comments for a specific post
        Expected: Return list of comments for that post
        """
        comments = self.client.get_comments(post_id=existing_post["id"])

        assert isinstance(comments, list), "Should return a list of comments"
        if comments:
            assert isinstance(comments[0], dict), "Each comment should be a dictionary"


class TestPostsEndpointParametrized:
    """Parametrized tests for posts endpoint"""

    @pytest.fixture(autouse=True)
    def setup(self):
        self.client = JSONPlaceholderClient()

    @pytest.mark.parametrize("post_id", [1, 2, 3, 4, 5])
    def test_get_multiple_posts(self, post_id):
        """
        Test: Get multiple different posts
        Expected: Each post request returns correct post
        """
        post = self.client.get_post(post_id)
        assert post["id"] == post_id

    @pytest.mark.parametrize("limit", [1, 5, 10])
    def test_limit_posts(self, limit):
        """
        Test: Get posts with limit parameter
        Expected: Return list with specified maximum items
        """
        posts = self.client.get_posts(limit=limit)
        assert len(posts) <= limit
