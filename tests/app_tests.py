import pytest
from django.urls import reverse
from rest_framework.exceptions import ValidationError


@pytest.mark.django_db
def test_create_board(client, user, board):
    expected_response = {
        "id": 2,
        "title": "test board",
        "is_deleted": False,
        "created": board.created.isoformat().replace('+00:00', '') + 'Z',
        "updated": board.updated.isoformat().replace('+00:00', '') + 'Z',
    }
    data = {
        "title": "test board",
        "is_deleted": False,
        "created": board.created.isoformat().replace('+00:00', '') + 'Z',
        "updated": board.updated.isoformat().replace('+00:00', '') + 'Z',
    }

    user.set_password(user.password)
    user.save()

    client.force_authenticate(user)
    response = client.post(
        '/goals/board/create',
        data=data
    )

    assert response.status_code == 201
    assert response.data["id"] == expected_response["id"]
    assert response.data["title"] == expected_response["title"]



@pytest.mark.django_db
def test_one_board(client, user, board):
    expected_response = {
        'id': board.pk,
        'title': board.title,
        'is_deleted': False,
    }

    user.set_password(user.password)
    user.save()

    client.force_authenticate(user)
    client.post(
        '/goals/board/create',
        data={
            "id": board.pk,
            "title": board.title,
            "is_deleted": board.is_deleted,
        }
    )

    response = client.get(f'/goals/board/{board.pk + 1}')

    assert response.status_code == 200
    assert response.data["id"] == expected_response["id"] + 1
    assert response.data["title"] == expected_response["title"]
    assert response.data["is_deleted"] == False



@pytest.mark.django_db
def test_cateogries_list(client, board_participant, goal_category):
    expected_response = {
        "id": goal_category.pk,
        "user": goal_category.user.id,
        "created": goal_category.created.isoformat().replace('+00:00', '') + 'Z',
        "updated": goal_category.updated.isoformat().replace('+00:00', '') + 'Z',
        "title": goal_category.title,
        "is_deleted": False,
        "board": goal_category.board.id,
    }

    user = board_participant.user
    user.set_password(user.password)
    user.save()

    client.force_authenticate(user)
    response_list = client.get('/goals/goal_category/list')

    assert response_list.status_code == 200
    assert response_list.data[0]["id"] == expected_response["id"]
    assert response_list.data[0]["title"] == expected_response["title"]
    assert response_list.data[0]["board"] == expected_response["board"]
    assert response_list.data[0]["user"]["id"] == expected_response["user"]


@pytest.mark.django_db
def test_one_category(client, board_participant, goal_category):
    expected_response = {
        "id": goal_category.pk,
        "title": goal_category.title,
        "user": goal_category.user.pk,
        "is_deleted": False,
        "board": goal_category.board.pk,
    }

    user = board_participant.user
    user.set_password(user.password)
    user.save()

    client.force_authenticate(user)

    response = client.get(f'/goals/goal_category/{goal_category.pk}')

    assert response.status_code == 200
    assert response.data["id"] == expected_response["id"]
    assert response.data["title"] == expected_response["title"]
    assert response.data["board"] == expected_response["board"]
    assert response.data["user"]["id"] == expected_response["user"]




@pytest.mark.django_db
def test_goal_list(client, board_participant, goal):
    expected_response = {
        "id": goal.pk,
        "user": goal.user.pk,
        "created": goal.created.isoformat().replace('+00:00', '') + 'Z',
        "updated": goal.updated.isoformat().replace('+00:00', '') + 'Z',
        "title": goal.title,
        "description": goal.description,
        "due_date": goal.due_date,
        "status": goal.status,
        "priority": goal.priority,
        "category": goal.category.pk,
    }
    user = board_participant.user
    user.set_password(user.password)
    user.save()

    client.force_authenticate(user)
    response_list = client.get('/goals/goal/list')

    assert response_list.status_code == 200
    assert response_list.data[0]["id"] == expected_response["id"]
    assert response_list.data[0]["title"] == expected_response["title"]
    assert response_list.data[0]["description"] == expected_response["description"]
    assert response_list.data[0]["category"] == expected_response["category"]
    assert response_list.data[0]["user"]["id"] == expected_response["user"]


@pytest.mark.django_db
def test_one_goal(client, board_participant, goal):
    expected_response = {
        "id": goal.pk,
        "user": goal.user.id,
        "created": goal.created.isoformat().replace('+00:00', '') + 'Z',
        "updated": goal.updated.isoformat().replace('+00:00', '') + 'Z',
        "title": goal.title,
        "description": goal.description,
        "due_date": goal.due_date,
        "status": goal.status,
        "priority": goal.priority,
        "category": goal.category.id,
    }

    user = board_participant.user

    user.set_password(user.password)
    user.save()

    client.force_authenticate(user)

    response = client.get(reverse('goal', kwargs={'pk': goal.id}))
    assert response.status_code == 200
    assert response.data["id"] == expected_response["id"]
    assert response.data["title"] == expected_response["title"]
    assert response.data["description"] == expected_response["description"]
    assert response.data["category"] == expected_response["category"]
    assert response.data["user"]["id"] == expected_response["user"]


@pytest.mark.django_db
def test_create_goal_comment(client, board_participant, goal_comment):
    expected_response = {
        "id": goal_comment.pk + 1,
        "created": goal_comment.created.isoformat().replace('+00:00', '') + 'Z',
        "updated": goal_comment.updated.isoformat().replace('+00:00', '') + 'Z',
        "text": goal_comment.text,
        "goal": goal_comment.goal.id,
    }
    data = {
        "text": "test comment",
        "user": board_participant.user.pk,
        "goal": goal_comment.goal.id,
    }

    user = board_participant.user
    user.set_password(user.password)
    user.save()

    client.force_authenticate(user)
    response = client.post(
        '/goals/goal_comment/create',
        data=data
    )

    assert response.status_code == 201
    assert response.data["id"] == expected_response["id"]
    assert response.data["text"] == expected_response["text"]
    assert response.data["goal"] == expected_response["goal"]


@pytest.mark.django_db
def test_goal_comment_list(client, board_participant, goal_comment):
    expected_response = {
        "id": goal_comment.pk,
        "user": goal_comment.user.pk,
        "created": goal_comment.created.isoformat().replace('+00:00', '') + 'Z',
        "updated": goal_comment.updated.isoformat().replace('+00:00', '') + 'Z',
        "text": goal_comment.text,
        "goal": goal_comment.goal.id,
    }

    user = board_participant.user
    user.set_password(user.password)
    user.save()

    client.force_authenticate(user)
    response_list = client.get('/goals/goal_comment/list')

    assert response_list.status_code == 200
    assert response_list.data[0]["id"] == expected_response["id"]
    assert response_list.data[0]["text"] == expected_response["text"]
    assert response_list.data[0]["goal"] == expected_response["goal"]
    assert response_list.data[0]["user"]["id"] == expected_response["user"]


@pytest.mark.django_db
def test_one_goal_comment(client, board_participant, goal_comment):
    expected_response = {
        "id": goal_comment.pk,
        "user": goal_comment.user.pk,
        "created": goal_comment.created.isoformat().replace('+00:00', '') + 'Z',
        "updated": goal_comment.updated.isoformat().replace('+00:00', '') + 'Z',
        "text": goal_comment.text,
        "goal": goal_comment.goal.pk,
    }

    user = board_participant.user
    user.set_password(user.password)
    user.save()

    client.force_authenticate(user)
    response = client.get(f'/goals/goal_comment/{goal_comment.pk}')

    assert response.status_code == 200
    assert response.data["id"] == expected_response["id"]
    assert response.data["text"] == expected_response["text"]
    assert response.data["goal"] == expected_response["goal"]
    assert response.data["user"]["id"] == expected_response["user"]