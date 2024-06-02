import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import app, get_db, Base

DATABASE_URL = "sqlite:///./test_test.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture(scope="function", autouse=True)
def setup_and_teardown_db():
    # 在每个测试之前重建数据库表
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    # 测试之后不需要特别处理，因为每个测试都会重建数据库

def get_token():
    response = client.post(
        "/token",
        data={"username": "user5", "password": "5"},
    )
    response_data = response.json()
    if "access_token" in response_data:
        return response_data["access_token"]
    else:
        raise ValueError("Failed to obtain access token")

@pytest.fixture
def token():
    # 先创建一个用户
    client.post(
        "/users/",
        json={"username": "user5", "email": "user5@example.com", "full_name": "User Two", "hashed_password": "5", "money": 1000},
    )
    return get_token()

def test_create_user():
    response = client.post(
        "/users/",
        json={"username": "user6", "email": "user6@example.com", "full_name": "User Six", "hashed_password": "6", "money": 1000},
    )
    assert response.status_code == 200

def test_read_user():
    client.post(
        "/users/",
        json={"username": "user5", "email": "user5@example.com", "full_name": "User Two", "hashed_password": "5", "money": 1000},
    )
    response = client.get(
        "/users/1"
    )
    assert response.status_code == 200
    


def test_create_ticket_event_not_found(token):
    # 尝试为不存在的事件购买票
    response = client.post(
        "/tickets/999",
        json={
            "number": 2,
            "name": "John Doe",
            "IDcard": "123456789012345678",
            "phonenumber": "1234567890"
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Event not found"

def test_create_ticket_tickets_sold_out(token):
    # 创建一个售罄的事件
    client.post(
        "/events/",
        json={
            "name": "Sold Out Concert",
            "event_time": "2024-07-01T20:00:00",
            "description": "Live concert event",
            "duration_hours": 3,
            "duration_minutes": 0,
            "price": 100,
            "tickets_sold": 50,
            "max_tickets": 50
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    # 尝试为售罄的事件购买票
    response = client.post(
        "/tickets/2",
        json={
            "number": 1,
            "name": "John Doe",
            "IDcard": "123456789012345678",
            "phonenumber": "1234567890"
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 404

def test_create_ticket_insufficient_funds(token):
    # 创建一个事件
    client.post(
        "/events/",
        json={
            "name": "Expensive Concert",
            "event_time": "2024-07-01T20:00:00",
            "description": "Live concert event",
            "duration_hours": 3,
            "duration_minutes": 0,
            "price": 1000,
            "tickets_sold": 0,
            "max_tickets": 50
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    # 尝试在余额不足的情况下购买票
    response = client.post(
        "/tickets/3",
        json={
            "number": 1,
            "name": "John Doe",
            "IDcard": "123456789012345678",
            "phonenumber": "1234567890"
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 404

def test_create_event(token):
    response = client.post(
        "/events/",
        json={
            "name": "Sample Event",
            "event_time": "2024-06-01T10:00:00",
            "description": "This is a sample event",
            "duration_hours": 2,
            "duration_minutes": 30,
            "price": 50,
            "tickets_sold": 0,
            "max_tickets": 100
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json()["name"] == "Sample Event"

def test_read_events():
    response = client.get("/events/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_update_event(token):
    client.post(
        "/events/",
        json={
            "name": "Sample Event",
            "event_time": "2024-06-01T10:00:00",
            "description": "This is a sample event",
            "duration_hours": 2,
            "duration_minutes": 30,
            "price": 50,
            "tickets_sold": 0,
            "max_tickets": 100
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    response = client.put(
        "/events/1",
        json={
            "name": "Updated Event",
            "event_time": "2024-06-01T10:00:00",
            "description": "This is an updated event",
            "duration_hours": 3,
            "duration_minutes": 0,
            "price": 60,
            "tickets_sold": 10,
            "max_tickets": 150
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json()["name"] == "Updated Event"

def test_delete_event(token):
    client.post(
        "/events/",
        json={
            "name": "Sample Event",
            "event_time": "2024-06-01T10:00:00",
            "description": "This is a sample event",
            "duration_hours": 2,
            "duration_minutes": 30,
            "price": 50,
            "tickets_sold": 0,
            "max_tickets": 100
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    response = client.delete(
        "/events/1",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json()["message"] == "Event deleted"

def test_create_notification(token):
    headers = {"Authorization": f"Bearer {token}"}
    response = client.post(
        "/notifications/",
        headers=headers,
        json={"message": "Test notification", "sender": "Test sender"}
    )
    assert response.status_code == 200
    response_data = response.json()
    assert "id" in response_data
    assert response_data["message"] == "Test notification"
    assert response_data["sender"] == "Test sender"

def test_read_notifications(token):
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get(
        "/notifications/",
        headers=headers
    )
    assert response.status_code == 200
    assert "notifications" in response.json()

def test_read_notification(token):
    headers = {"Authorization": f"Bearer {token}"}
    response = client.post(
        "/notifications/",
        headers=headers,
        json={"message": "Test notification", "sender": "Test sender"}
    )
    assert response.status_code == 200
    response_data = response.json()
    assert "id" in response_data
    assert response_data["message"] == "Test notification"
    assert response_data["sender"] == "Test sender"
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get(
        "/notifications/1",
        headers=headers
    )
    assert response.status_code == 200
    assert "id" in response.json()

def test_mark_all_notifications_read(token):
    headers = {"Authorization": f"Bearer {token}"}
    response = client.put(
        "/notifications/mark_all_read",
        headers=headers
    )
    assert response.status_code == 200
    assert response.json() == {"detail": "All notifications marked as read"}


def test_create_post(token):
    response = client.post(
        "/posts/",
        json={
            "title": "First Post",
            "content": "This is the content of the first post"
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json()["title"] == "First Post"


def test_create_comment(token):
    # 先创建一个事件
    client.post(
        "/events/",
        json={
            "name": "Sample Event",
            "event_time": "2024-06-01T10:00:00",
            "description": "This is a sample event",
            "duration_hours": 2,
            "duration_minutes": 30,
            "price": 50,
            "tickets_sold": 0,
            "max_tickets": 100
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    response = client.post(
        "/comments/1",
        json={
            "content": "This is a comment for the event"
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200

def test_read_comments():
    # 先创建一个事件
    client.post(
        "/events/",
        json={
            "name": "Sample Event",
            "event_time": "2024-06-01T10:00:00",
            "description": "This is a sample event",
            "duration_hours": 2,
            "duration_minutes": 30,
            "price": 50,
            "tickets_sold": 0,
            "max_tickets": 100
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    # 创建评论
    client.post(
        "/comments/1",
        json={
            "content": "This is a comment for the event"
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    response = client.get("/comments/1")
    assert response.status_code == 200

def test_create_post_comment(token):
    # 先创建一个帖子
    client.post(
        "/posts/",
        json={
            "title": "First Post",
            "content": "This is the content of the first post"
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    response = client.post(
        "/post_comments/1",
        json={
            "content": "This is a comment for the post"
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200

def test_read_post_comments():
    # 先创建一个帖子
    client.post(
        "/posts/",
        json={
            "title": "First Post",
            "content": "This is the content of the first post"
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    # 创建帖子评论
    client.post(
        "/post_comments/1",
        json={
            "content": "This is a comment for the post"
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    response = client.get("/post_comments/1")
    assert response.status_code == 200


def test_read_posts():
    response = client.get("/posts/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_read_post():
    # 先创建一个帖子
    client.post(
        "/posts/",
        json={
            "title": "First Post",
            "content": "This is the content of the first post"
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    
    response = client.get("/posts/")
    assert response.status_code == 200
