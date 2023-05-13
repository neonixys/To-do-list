import pytest

from rest_framework.test import APIClient
from pytest_factoryboy import register

from tests.factories import BoardFactory, GoalCategoryFactory, GoalFactory, GoalCommentFactory, UserFactory, \
    BoardParticipantFactory

pytest_plugins = 'tests.factories'


@pytest.fixture()
def client() -> APIClient:
    """"Rest Framework tests client instance."""
    return APIClient()


@pytest.fixture()
def aut_client(client, user):
    client.force_login(user)
    return client


pytest_plugins = "tests.fixtures"

register(UserFactory)
register(BoardFactory)
register(BoardParticipantFactory)
register(GoalCategoryFactory)
register(GoalFactory)
register(GoalCommentFactory)