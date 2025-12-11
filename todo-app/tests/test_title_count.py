"""Tests for browser title todo count feature."""

import pytest

from app.database import Todo


class TestBrowserTitleCount:
    """Tests for the browser title todo count functionality."""

    def test_page_title_includes_incomplete_count(self, authenticated_client, test_list, db_session):
        """Test that page title includes incomplete todo count when count > 0."""
        # Create 3 incomplete todos
        for i in range(3):
            todo = Todo(
                list_id=test_list.id,
                title=f"Todo {i+1}",
                position=i,
                is_completed=False,
            )
            db_session.add(todo)
        db_session.commit()

        # Get the list page
        response = authenticated_client.get(f"/app/lists/{test_list.id}")
        assert response.status_code == 200
        
        # Check that title includes count
        assert f"(3) {test_list.name} - Todo App" in response.text

    def test_page_title_without_count_when_all_complete(self, authenticated_client, test_list, db_session):
        """Test that page title doesn't include count when all todos are complete."""
        # Create 2 completed todos
        for i in range(2):
            todo = Todo(
                list_id=test_list.id,
                title=f"Todo {i+1}",
                position=i,
                is_completed=True,
            )
            db_session.add(todo)
        db_session.commit()

        # Get the list page
        response = authenticated_client.get(f"/app/lists/{test_list.id}")
        assert response.status_code == 200
        
        # Check that title doesn't include count (no parentheses)
        assert f"{test_list.name} - Todo App" in response.text
        assert "(0)" not in response.text

    def test_page_title_without_count_when_empty(self, authenticated_client, test_list):
        """Test that page title doesn't include count when list is empty."""
        # Get the list page (no todos)
        response = authenticated_client.get(f"/app/lists/{test_list.id}")
        assert response.status_code == 200
        
        # Check that title doesn't include count
        assert f"{test_list.name} - Todo App" in response.text
        assert "(0)" not in response.text

    def test_page_title_with_mixed_todos(self, authenticated_client, test_list, db_session):
        """Test that page title shows only incomplete todo count."""
        # Create 2 incomplete and 3 complete todos
        for i in range(5):
            todo = Todo(
                list_id=test_list.id,
                title=f"Todo {i+1}",
                position=i,
                is_completed=(i >= 2),  # First 2 incomplete, last 3 complete
            )
            db_session.add(todo)
        db_session.commit()

        # Get the list page
        response = authenticated_client.get(f"/app/lists/{test_list.id}")
        assert response.status_code == 200
        
        # Check that title includes count of incomplete todos only
        assert f"(2) {test_list.name} - Todo App" in response.text

    def test_oob_swap_includes_title_count_on_toggle(self, authenticated_client, test_list, db_session):
        """Test that OOB swap includes page title count update when toggling a todo."""
        # Create an incomplete todo
        todo = Todo(
            list_id=test_list.id,
            title="Test Todo",
            position=0,
            is_completed=False,
        )
        db_session.add(todo)
        db_session.commit()

        # Toggle the todo to completed
        response = authenticated_client.patch(f"/api/todos/{todo.id}/toggle")
        assert response.status_code == 200
        
        # Check that response includes OOB swap for page title count
        assert 'id="page-title-count"' in response.text
        assert 'hx-swap-oob="true"' in response.text
        assert 'data-count="0"' in response.text

    def test_oob_swap_includes_title_count_on_create(self, authenticated_client, test_list):
        """Test that OOB swap includes page title count update when creating a todo."""
        # Create a new todo
        response = authenticated_client.post(
            "/api/todos",
            data={
                "list_id": test_list.id,
                "title": "New Todo",
            },
        )
        assert response.status_code == 200
        
        # Check that response includes OOB swap for page title count
        assert 'id="page-title-count"' in response.text
        assert 'hx-swap-oob="true"' in response.text
        assert 'data-count="1"' in response.text

    def test_oob_swap_includes_title_count_on_delete(self, authenticated_client, test_list, db_session):
        """Test that OOB swap includes page title count update when deleting a todo."""
        # Create an incomplete todo
        todo = Todo(
            list_id=test_list.id,
            title="Test Todo",
            position=0,
            is_completed=False,
        )
        db_session.add(todo)
        db_session.commit()

        # Delete the todo
        response = authenticated_client.delete(f"/api/todos/{todo.id}")
        assert response.status_code == 200
        
        # Check that response includes OOB swap for page title count
        assert 'id="page-title-count"' in response.text
        assert 'hx-swap-oob="true"' in response.text
        assert 'data-count="0"' in response.text
