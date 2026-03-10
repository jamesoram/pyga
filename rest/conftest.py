"""
Pytest fixtures for API testing
Reusable fixtures for JSONPlaceholder API testing
"""

import pytest
import random
from api_client import JSONPlaceholderClient


@pytest.fixture(scope="module")
def api_client():
    return JSONPlaceholderClient()


@pytest.fixture(scope="module")
def test_data_manager(api_client):
    created_resources = {'posts': []}
    
    class TestDataManager:
        def __init__(self, client):
            self.client = client
        
        def create_post(self, **kwargs):
            post = self.client.create_post(kwargs["title"], kwargs["body"], kwargs["userId"])
            created_resources['posts'].append(post['id'])
            return post
        
        def cleanup(self):
            for post_id in created_resources['posts']:
                try:
                    self.client.delete_post(post_id)
                except Exception:
                    pass
            created_resources['posts'].clear()
    
    manager = TestDataManager(api_client)
    yield manager
    manager.cleanup()


@pytest.fixture
def random_suffix():
    return str(random.randint(1000, 9999))


@pytest.fixture
def sample_post_data(random_suffix):
    return {
        "title": f"Test Post {random_suffix}",
        "body": f"This is the content of test post {random_suffix}",
        "userId": 1,
    }


@pytest.fixture
def new_post(api_client, sample_post_data):
    post = api_client.create_post(
        sample_post_data["title"], sample_post_data["body"], sample_post_data["userId"]
    )
    yield post
    api_client.delete_post(post["id"])


@pytest.fixture
def existing_post(api_client):
    posts = api_client.get_posts(limit=1)
    if posts:
        return posts[0]
    pytest.skip("No existing posts found")


@pytest.fixture
def post_lifecycle(api_client, sample_post_data):
    post = api_client.create_post(
        sample_post_data["title"], sample_post_data["body"], sample_post_data["userId"]
    )
    yield post
    api_client.delete_post(post["id"])


@pytest.fixture
def multiple_posts(test_data_manager, random_suffix):
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
def sample_patch_data():
    return {"title": "Updated Title"}


@pytest.fixture
def post_with_comments(api_client, new_post, random_suffix):
    for i in range(2):
        api_client.create_comment(
            new_post["id"],
            f"Commenter {i}",
            f"commenter{i}@test.com",
            f"Comment content {i}"
        )
    return new_post
