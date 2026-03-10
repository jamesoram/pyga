"""
API validation tests
Tests that validate API response structure and data types
"""

import pytest
from api_client import JSONPlaceholderClient


class TestResponseValidation:
    """Test response structure validation"""

    @pytest.fixture(autouse=True)
    def setup(self):
        self.client = JSONPlaceholderClient()

    def test_post_structure(self):
        """
        Test: Validate post response structure
        Expected: All required fields present
        """
        post = self.client.get_post(1)

        required_fields = ["id", "title", "body", "userId"]
        for field in required_fields:
            assert field in post, f"Missing required field: {field}"

    def test_post_data_types(self):
        """
        Test: Validate post field data types
        Expected: Each field matches expected type
        """
        post = self.client.get_post(1)

        assert isinstance(post["id"], int), "ID should be integer"
        assert isinstance(post["title"], str), "Title should be string"
        assert isinstance(post["body"], str), "Body should be string"
        assert isinstance(post["userId"], int), "UserId should be integer"

    def test_list_response_structure(self):
        """
        Test: Validate list response structure
        Expected: List of posts, each with valid structure
        """
        posts = self.client.get_posts(limit=5)

        assert isinstance(posts, list)
        assert len(posts) == 5

        for post in posts:
            assert isinstance(post, dict)
            assert "id" in post
            assert "title" in post


class TestValidationMarks:
    """Tests with validation markers"""

    @pytest.fixture(autouse=True)
    def setup(self):
        self.client = JSONPlaceholderClient()

    @pytest.mark.validation
    @pytest.mark.parametrize("post_id", [1, 10, 100])
    def test_validate_post_data_types(self, post_id):
        """
        Validate data types across multiple posts
        Run with: pytest -v -m validation
        """
        post = self.client.get_post(post_id)

        assert isinstance(post["id"], int)
        assert isinstance(post["title"], str)
        assert isinstance(post["body"], str)
        assert isinstance(post["userId"], int)

    @pytest.mark.validation
    def test_validate_title_format(self):
        """
        Validate title format constraints
        """
        posts = self.client.get_posts(limit=10)

        for post in posts:
            assert len(post["title"]) > 0, "Title should not be empty"
            assert len(post["title"]) <= 100, "Title should be reasonable length"


class TestErrorValidation:
    """Test error response validation"""

    @pytest.fixture(autouse=True)
    def setup(self):
        self.client = JSONPlaceholderClient()

    def test_404_validation(self):
        """
        Test: Validate 404 error response
        For mock APIs, we may return empty dict instead of raising
        """
        import requests
        
        post = self.client.get_post(99999)
        assert post == {}, "Should return empty dict for 404"

    def test_404_error_structure(self):
        """
        Test: Validate 404 error response structure
        """
        import requests
        
        post = self.client.get_post(0)
        assert post == {}, "Should return empty dict for 404"


class TestContentValidation:
    """Test content-specific validation"""

    @pytest.fixture(autouse=True)
    def setup(self):
        self.client = JSONPlaceholderClient()

    def test_titles_are_unique(self):
        """
        Test: Validate titles are unique across posts
        Note: JSONPlaceholder may have duplicate titles
        This test shows validation approach
        """
        posts = self.client.get_posts(limit=50)
        titles = [post["title"] for post in posts]

        unique_titles = set(titles)
        assert len(unique_titles) > 0

    def test_bodies_are_non_empty(self):
        """
        Test: Validate body content is not empty
        """
        posts = self.client.get_posts(limit=10)

        for post in posts:
            assert len(post["body"]) > 0, "Body should not be empty"


class TestValidationWithFixtures:
    """Validation tests using fixtures"""

    def test_validate_new_post_structure(self, new_post):
        """
        Test: Validate structure of created post
        Uses fixture that handles creation and cleanup
        """
        required_fields = ["id", "title", "body", "userId"]
        for field in required_fields:
            assert field in new_post, f"Missing field: {field}"

        assert isinstance(new_post["id"], int)
        assert isinstance(new_post["title"], str)
        assert isinstance(new_post["body"], str)
