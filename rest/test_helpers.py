"""
API test assertions and helper functions
Custom assertions and utilities for API testing
"""

import pytest
from api_client import JSONPlaceholderClient
from typing import Dict, List, Any


class APIAssert:
    """
    Custom assertion class for API testing
    Provides domain-specific assertion methods
    """

    def __init__(self, client: JSONPlaceholderClient):
        self.client = client

    def assert_post_has_fields(
        self, post: Dict[str, Any], expected_fields: List[str]
    ) -> None:
        """
        Assert that post contains all expected fields

        Args:
            post: Post dictionary to validate
            expected_fields: List of expected field names
        """
        for field in expected_fields:
            assert field in post, f"Post missing field: {field}"

    def assert_post_data_matches(
        self, post: Dict[str, Any], expected_data: Dict[str, Any]
    ) -> None:
        """
        Assert that post data matches expected values

        Args:
            post: Actual post data
            expected_data: Dictionary of expected key-value pairs
        """
        for key, expected_value in expected_data.items():
            actual_value = post.get(key)
            assert actual_value == expected_value, (
                f"Field '{key}' mismatch: expected '{expected_value}', got '{actual_value}'"
            )

    def assert_list_has_length(self, items: List[Any], expected_length: int) -> None:
        """
        Assert that list has expected length

        Args:
            items: List to check
            expected_length: Expected number of items
        """
        assert len(items) == expected_length, (
            f"Expected {expected_length} items, got {len(items)}"
        )

    def assert_status_code(self, response, expected_status: int) -> None:
        """
        Assert response status code

        Args:
            response: Requests response object
            expected_status: Expected HTTP status code
        """
        assert response.status_code == expected_status, (
            f"Expected status {expected_status}, got {response.status_code}"
        )


@pytest.fixture
def api_assert(api_client):
    """
    Fixture providing APIAssert helper
    """
    return APIAssert(api_client)


class TestCustomAssertions:
    """Tests using custom assertions"""

    @pytest.fixture(autouse=True)
    def setup(self, api_assert):
        self.assert_api = api_assert

    def test_custom_assert_fields(self):
        """Test using custom field assertion"""
        post = self.assert_api.client.get_post(1)
        required_fields = ["id", "title", "body", "userId"]

        self.assert_api.assert_post_has_fields(post, required_fields)

    def test_custom_assert_data_match(self, sample_post_data):
        """Test using custom data comparison assertion"""
        post = self.assert_api.client.create_post(
            sample_post_data["title"],
            sample_post_data["body"],
            sample_post_data["userId"],
        )

        expected_data = {
            "title": sample_post_data["title"],
            "body": sample_post_data["body"],
            "userId": sample_post_data["userId"],
        }
        self.assert_api.assert_post_data_matches(post, expected_data)

        # Cleanup
        self.assert_api.client.delete_post(post["id"])

    def test_custom_assert_list_length(self):
        """Test using custom list length assertion"""
        posts = self.assert_api.client.get_posts(limit=5)

        self.assert_api.assert_list_has_length(posts, 5)


class TestHelperFunctions:
    """Tests demonstrating helper functions"""

    def test_find_post_by_title(self, api_client):
        """
        Find a post by title substring
        """
        posts = api_client.get_posts(limit=10)

        # Find post with specific title
        target_title = (
            "sunt aut facere repellat provident occaecati excepturi optio reprehenderit"
        )
        found_post = None
        for post in posts:
            if target_title[:20] in post["title"]:
                found_post = post
                break

        assert found_post is not None, "Should find a matching post"
        assert "title" in found_post

    def test_filter_posts_by_user(self, api_client):
        """
        Filter posts by user ID
        """
        posts = api_client.get_posts()

        user_id = 1
        user_posts = [post for post in posts if post["userId"] == user_id]

        assert len(user_posts) > 0, f"Should have posts for user {user_id}"

        for post in user_posts:
            assert post["userId"] == user_id
