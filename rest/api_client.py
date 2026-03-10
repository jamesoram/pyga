"""
API Client for JSONPlaceholder
A REST API for testing purposes
"""

import requests
from typing import Optional, Dict, Any, List


class JSONPlaceholderClient:
    """Client for JSONPlaceholder API"""

    BASE_URL = "https://jsonplaceholder.typicode.com"

    def __init__(self, timeout: int = 10):
        self.timeout = timeout
        self.session = requests.Session()

    def _build_url(self, endpoint: str) -> str:
        return f"{self.BASE_URL}/{endpoint}"

    def _handle_response(self, response: requests.Response) -> Dict[str, Any]:
        response.raise_for_status()
        return response.json()

    def get_posts(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Get all posts with optional limit
        """
        params = {"_limit": limit} if limit else {}
        response = self.session.get(
            self._build_url("posts"), params=params, timeout=self.timeout
        )
        json_data = response.json()
        if isinstance(json_data, list):
            return json_data
        return []

    def get_post(self, post_id: int) -> Dict[str, Any]:
        """
        Get a single post by ID
        
        Returns empty dict if post not found (404)
        """
        response = self.session.get(
            self._build_url(f"posts/{post_id}"), timeout=self.timeout
        )
        if response.status_code == 404:
            return {}
        response.raise_for_status()
        return response.json()

    def create_post(self, title: str, body: str, user_id: int) -> Dict[str, Any]:
        """
        Create a new post
        """
        payload = {"title": title, "body": body, "userId": user_id}
        response = self.session.post(
            self._build_url("posts"), json=payload, timeout=self.timeout
        )
        return response.json()

    def update_post(self, post_id: int, title: str, body: str) -> Dict[str, Any]:
        """
        Update a post (PUT - full update)
        """
        payload = {
            "id": post_id,
            "title": title,
            "body": body,
            "userId": 1,
        }
        response = self.session.put(
            self._build_url(f"posts/{post_id}"), json=payload, timeout=self.timeout
        )
        return response.json()

    def patch_post(
        self, post_id: int, title: Optional[str] = None, body: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Partially update a post (PATCH)
        """
        payload = {}
        if title:
            payload["title"] = title
        if body:
            payload["body"] = body

        response = self.session.patch(
            self._build_url(f"posts/{post_id}"), json=payload, timeout=self.timeout
        )
        return response.json()

    def delete_post(self, post_id: int) -> bool:
        """
        Delete a post
        """
        response = self.session.delete(
            self._build_url(f"posts/{post_id}"), timeout=self.timeout
        )
        # JSONPlaceholder returns 404 for delete (simulated)
        return response.status_code in [200, 404]

    def get_comments(
        self, post_id: Optional[int] = None, limit: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Get comments, optionally filtered by post
        """
        endpoint = "comments"
        if post_id:
            endpoint = f"posts/{post_id}/comments"

        params = {"_limit": limit} if limit else {}
        response = self.session.get(
            self._build_url(endpoint), params=params, timeout=self.timeout
        )
        json_data = response.json()
        if isinstance(json_data, list):
            return json_data
        return []

    def create_comment(
        self, post_id: int, name: str, email: str, body: str
    ) -> Dict[str, Any]:
        """
        Create a comment for a post
        """
        payload = {
            "postId": post_id,
            "name": name,
            "email": email,
            "body": body,
        }
        response = self.session.post(
            self._build_url("comments"), json=payload, timeout=self.timeout
        )
        return response.json()
