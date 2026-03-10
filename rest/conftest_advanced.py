"""
Pytest fixtures for API testing with database-like operations
Advanced fixtures for test data management and cleanup
"""

import pytest
import random
from api_client import JSONPlaceholderClient


@pytest.fixture(scope="module")
def api_client():
    """
    Module-scoped API client
    One client shared across all tests in a module
    """
    return JSONPlaceholderClient()


@pytest.fixture(scope="module")
def test_data_manager(api_client):
    """
    Manage test data lifecycle across module
    Tracks created resources for cleanup
    """
    created_resources = {"posts": [], "comments": []}

    class TestDataManager:
        def __init__(self, client):
            self.client = client

        def create_post(self, **kwargs):
            """Create a post and track it for cleanup"""
            post = self.client.create_post(**kwargs)
            created_resources["posts"].append(post["id"])
            return post

        def create_comment(self, post_id, **kwargs):
            """Create a comment and track it for cleanup"""
            comment = self.client.create_comment(post_id, **kwargs)
            created_resources["comments"].append(comment["id"])
            return comment

        def cleanup(self):
            """Delete all created resources"""
            for post_id in created_resources["posts"]:
                try:
                    self.client.delete_post(post_id)
                except Exception:
                    pass  # Ignore if already deleted
            created_resources["posts"].clear()

    manager = TestDataManager(api_client)
    yield manager
    # Cleanup after all tests in module complete
    manager.cleanup()


@pytest.fixture
def random_suffix():
    """Generate random suffix for unique test data"""
    return str(random.randint(10000, 99999))


@pytest.fixture
def sample_post_data(random_suffix):
    """Generate sample post data"""
    return {
        "title": f"Test Post {random_suffix}",
        "body": f"Post content {random_suffix}",
        "userId": 1,
    }


@pytest.fixture
def new_post(test_data_manager, sample_post_data):
    """
    Create a post using test data manager
    Automatically tracked for cleanup
    """
    return test_data_manager.create_post(**sample_post_data)


@pytest.fixture
def multiple_posts(test_data_manager, random_suffix):
    """
    Create multiple posts for testing
    Returns list of posts
    """
    posts = []
    for i in range(3):
        post_data = {
            "title": f"Batch Post {random_suffix} - {i}",
            "body": f"Content {i}",
            "userId": 1,
        }
        post = test_data_manager.create_post(**post_data)
        posts.append(post)
    return posts


@pytest.fixture
def post_lifecycle(api_client, sample_post_data):
    """
    Test post lifecycle: create, modify, delete
    Yields post through lifecycle stages
    """
    # Create
    post = api_client.create_post(
        sample_post_data["title"], sample_post_data["body"], sample_post_data["userId"]
    )
    yield post

    # Cleanup (runs after test completes)
    api_client.delete_post(post["id"])


@pytest.fixture
def post_with_comments(api_client, new_post, random_suffix):
    """
    Create a post with multiple comments
    Useful for testing nested data structures
    """
    # Add a few comments to the post
    for i in range(2):
        api_client.create_comment(
            new_post["id"],
            name=f"Commenter {i}",
            email=f"commenter{i}@test.com",
            body=f"Comment content {i}",
        )
    return new_post
