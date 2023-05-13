import pytest

from to_do_list.core.models import User
from to_do_list.goals.models import Board, BoardParticipant, GoalCategory, Goal, GoalComment


@pytest.mark.django_db
def test_board_creation():
    title = "Test Board"
    board = Board.objects.create(title=title)
    assert board.title == title


@pytest.mark.django_db
def test_board_participant_creation():
    board = Board.objects.create(title="Test Board")
    user = User.objects.create(username="Test User")
    role = BoardParticipant.Role.reader
    participant = BoardParticipant.objects.create(board=board, user=user, role=role)
    assert participant.board == board
    assert participant.user == user
    assert participant.role == role


@pytest.mark.django_db
def test_goal_category_creation():
    user = User.objects.create(username="Test User")
    board = Board.objects.create(title="Test Board")
    title = "Test Category"
    category = GoalCategory.objects.create(title=title, user=user, board=board)
    assert category.title == title
    assert category.user == user
    assert category.board == board


@pytest.mark.django_db
def test_goal_creation():
    user = User.objects.create(username="Test User")
    board = Board.objects.create(title="Test Board")
    category = GoalCategory.objects.create(title="Test Category", user=user, board=board)
    title = "Test Goal"
    goal = Goal.objects.create(title=title, category=category, user=user)
    assert goal.title == title
    assert goal.category == category
    assert goal.user == user


@pytest.mark.django_db
def test_goal_comment_creation():
    user = User.objects.create(username="Test User")
    board = Board.objects.create(title="Test Board")
    category = GoalCategory.objects.create(title="Test Category", user=user, board=board)
    goal = Goal.objects.create(title="Test Goal", category=category, user=user)
    text = "Test Comment"
    comment = GoalComment.objects.create(text=text, user=user, goal=goal)
    assert comment.text == text
    assert comment.user == user
    assert comment.goal == goal


@pytest.mark.django_db
def test_goal_category_deletion():
    user = User.objects.create(username="Test User")
    board = Board.objects.create(title="Test Board")
    category = GoalCategory.objects.create(title="Test Category", user=user, board=board)
    category.is_deleted = True
    assert category.is_deleted


@pytest.mark.django_db
def test_goal_deletion():
    user = User.objects.create(username="Test User")
    board = Board.objects.create(title="Test Board")
    category = GoalCategory.objects.create(title="Test Category", user=user, board=board)
    goal = Goal.objects.create(title="Test Goal", category=category, user=user)
    goal.delete()
    assert GoalCategory.objects.filter(goals=goal).exists()
