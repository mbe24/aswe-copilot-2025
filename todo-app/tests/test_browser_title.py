"""Tests for browser tab title feature."""

import re

import pytest

from app.database import TodoList


class TestBrowserTitle:
    """Test browser tab title updates with incomplete todo count."""

    def test_title_without_incomplete_todos(self, client, db_session, authenticated_client):
        """Test title shows list name without count when no incomplete todos."""
        # Create a list
        response = authenticated_client.post(
            "/api/lists",
            data={
                "name": "Shopping",
                "description": "Grocery list",
                "color": "#3b82f6",
            },
        )
        assert response.status_code == 200

        # Get the list
        todo_list = db_session.query(TodoList).filter(TodoList.name == "Shopping").first()
        assert todo_list is not None

        # Get the app page for this list
        response = authenticated_client.get(f"/app/lists/{todo_list.id}")
        assert response.status_code == 200
        assert b"<title>Shopping - Todo App</title>" in response.content

    def test_title_with_incomplete_todos(self, client, db_session, authenticated_client):
        """Test title shows count when there are incomplete todos."""
        # Create a list
        response = authenticated_client.post(
            "/api/lists",
            data={
                "name": "Work Tasks",
                "description": "Work todos",
                "color": "#ef4444",
            },
        )
        assert response.status_code == 200

        # Get the list
        todo_list = db_session.query(TodoList).filter(TodoList.name == "Work Tasks").first()
        assert todo_list is not None

        # Add 3 incomplete todos
        for i in range(3):
            response = authenticated_client.post(
                "/api/todos",
                data={
                    "list_id": todo_list.id,
                    "title": f"Task {i+1}",
                },
            )
            assert response.status_code == 200

        # Get the app page for this list
        response = authenticated_client.get(f"/app/lists/{todo_list.id}")
        assert response.status_code == 200
        assert b"<title>(3) Work Tasks - Todo App</title>" in response.content

    def test_title_with_some_completed_todos(self, client, db_session, authenticated_client):
        """Test title shows only incomplete todo count."""
        # Create a list
        response = authenticated_client.post(
            "/api/lists",
            data={
                "name": "Project",
                "description": "Project tasks",
                "color": "#10b981",
            },
        )
        assert response.status_code == 200

        # Get the list
        todo_list = db_session.query(TodoList).filter(TodoList.name == "Project").first()
        assert todo_list is not None

        # Add 5 todos
        todo_ids = []
        for i in range(5):
            response = authenticated_client.post(
                "/api/todos",
                data={
                    "list_id": todo_list.id,
                    "title": f"Task {i+1}",
                },
            )
            assert response.status_code == 200
            # Extract todo ID from response (it's in the HTML)
            html = response.text
            match = re.search(r'id="todo-([^"]+)"', html)
            if match:
                todo_ids.append(match.group(1))

        # Complete 3 todos
        for todo_id in todo_ids[:3]:
            response = authenticated_client.patch(f"/api/todos/{todo_id}/toggle")
            assert response.status_code == 200

        # Get the app page for this list - should show 2 incomplete
        response = authenticated_client.get(f"/app/lists/{todo_list.id}")
        assert response.status_code == 200
        assert b"<title>(2) Project - Todo App</title>" in response.content
