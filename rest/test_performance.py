"""
Performance and load testing for API
Tests for response times and concurrent requests
"""

import pytest
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from api_client import JSONPlaceholderClient


class TestPerformance:
    """Performance tests for API"""

    @pytest.fixture(autouse=True)
    def setup(self):
        self.client = JSONPlaceholderClient()

    def test_response_time_get_post(self):
        """
        Test: Response time for single post retrieval
        Expected: Response in under 1000ms
        """
        start_time = time.time()
        post = self.client.get_post(1)
        end_time = time.time()

        response_time = (end_time - start_time) * 1000  # Convert to ms

        print(f"\nResponse time: {response_time:.2f}ms")
        assert response_time < 1000, (
            f"Response took {response_time}ms, expected < 1000ms"
        )
        assert post["id"] == 1

    def test_response_time_get_posts(self):
        """
        Test: Response time for multiple posts
        """
        start_time = time.time()
        posts = self.client.get_posts(limit=10)
        end_time = time.time()

        response_time = (end_time - start_time) * 1000

        print(f"Response time for 10 posts: {response_time:.2f}ms")
        assert len(posts) == 10
        assert response_time < 2000

    def test_response_time_create_post(self):
        """
        Test: Response time for post creation
        """
        start_time = time.time()
        post = self.client.create_post("Performance Test", "Testing performance", 1)
        end_time = time.time()

        response_time = (end_time - start_time) * 1000

        print(f"Create time: {response_time:.2f}ms")
        assert "id" in post
        assert response_time < 2000

    def test_response_time_delete_post(self, new_post):
        """
        Test: Response time for post deletion
        """
        start_time = time.time()
        result = self.client.delete_post(new_post["id"])
        end_time = time.time()

        response_time = (end_time - start_time) * 1000

        print(f"Delete time: {response_time:.2f}ms")
        assert result
        assert response_time < 1000


class TestConcurrentRequests:
    """Tests for concurrent request handling"""

    @pytest.fixture(autouse=True)
    def setup(self):
        self.client = JSONPlaceholderClient()

    def test_concurrent_get_posts(self):
        """
        Test: Multiple concurrent GET requests
        """

        def fetch_post(post_id):
            return self.client.get_post(post_id)

        post_ids = [1, 2, 3, 4, 5]
        start_time = time.time()

        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(fetch_post, pid) for pid in post_ids]
            results = [f.result() for f in as_completed(futures)]

        end_time = time.time()
        total_time = (end_time - start_time) * 1000

        print(f"\nConcurrent requests time: {total_time:.2f}ms")

        assert len(results) == 5
        assert all(r["id"] in post_ids for r in results)

    def test_concurrent_create_posts(self, sample_post_data):
        """
        Test: Multiple concurrent POST requests
        """

        def create_post(title_suffix):
            data = sample_post_data.copy()
            data["title"] = f"{sample_post_data['title']} - {title_suffix}"
            return self.client.create_post(data["title"], data["body"], data["userId"])

        start_time = time.time()

        with ThreadPoolExecutor(max_workers=3) as executor:
            futures = [executor.submit(create_post, i) for i in range(3)]
            results = [f.result() for f in as_completed(futures)]

        end_time = time.time()
        total_time = (end_time - start_time) * 1000

        print(f"Concurrent creates time: {total_time:.2f}ms")

        assert len(results) == 3
        assert all("id" in r for r in results)

        # Cleanup
        for post in results:
            self.client.delete_post(post["id"])

    def test_request_ramp_up(self):
        """
        Test: Gradually increasing concurrent requests
        """

        def fetch_post(post_id):
            return self.client.get_post(post_id)

        results = []
        for num_workers in [1, 2, 4, 8]:
            start_time = time.time()

            with ThreadPoolExecutor(max_workers=num_workers) as executor:
                post_ids = list(range(1, num_workers + 1))
                futures = [executor.submit(fetch_post, pid) for pid in post_ids]
                results = [f.result() for f in as_completed(futures)]

            end_time = time.time()
            elapsed = (end_time - start_time) * 1000

            print(f"Workers: {num_workers}, Time: {elapsed:.2f}ms")

        assert len(results) > 0


class TestRateLimiting:
    """Test API rate limiting behavior"""

    @pytest.fixture(autouse=True)
    def setup(self):
        self.client = JSONPlaceholderClient()

    def test_many_requests(self):
        """
        Test: Many sequential requests
        JSONPlaceholder has no strict rate limits, but we test the pattern
        """
        start_time = time.time()

        for i in range(20):
            self.client.get_post((i % 10) + 1)

        end_time = time.time()
        total_time = (end_time - start_time) * 1000

        avg_time = total_time / 20
        print(f"\n20 requests, total: {total_time:.2f}ms, avg: {avg_time:.2f}ms each")

        assert total_time < 10000  # Should complete in under 10 seconds


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
