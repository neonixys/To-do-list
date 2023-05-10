from typing import Any

from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated, SAFE_METHODS, BasePermission
from rest_framework.request import Request

from to_do_list.goals.models import BoardParticipant, GoalCategory, GoalComment


class BoardPermissions(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        if request.method in permissions.SAFE_METHODS:
            return BoardParticipant.objects.filter(
                user=request.user, board=obj
            ).exists()
        return BoardParticipant.objects.filter(
            user=request.user, board=obj, role=BoardParticipant.Role.owner
        ).exists()


class GoalCategoryPermissions(IsAuthenticated):
    def has_object_permission(self, request: Request, view, goal_gategory: GoalCategory) -> bool:
        _filters: dict[str: Any] = {'user_id': request.user.id, 'board_id': goal_gategory.board_id}
        if request.method not in SAFE_METHODS:
            _filters['role'] = BoardParticipant.Role.owner

        return BoardParticipant.objects.filter(**_filters).exists()


class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.user.id == request.user.id


class GoalPermissions(IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        _filters: dict = {'user': request.user, 'board': obj.category.board}
        if request.method not in SAFE_METHODS:
            _filters['role__in'] = [BoardParticipant.Role.owner, BoardParticipant.Role.writer]

        return BoardParticipant.objects.filter(**_filters).exists()


class CommentPermissions(permissions.IsAuthenticated):
    def has_object_permission(self, request: Request, view: Any, obj: GoalComment) -> bool:
        return request.method in permissions.SAFE_METHODS or BoardParticipant.objects.filter(
            user=request.user,
            board=obj.goal.category.board,
            role__in=[BoardParticipant.Role.owner, BoardParticipant.Role.writer]
        ).exists()
