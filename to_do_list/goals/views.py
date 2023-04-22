from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions
from rest_framework.filters import OrderingFilter, SearchFilter

from to_do_list.goals.models import GoalCategory, Goal, GoalComment, BoardParticipant, Board
from to_do_list.goals.permissions import BoardPermissions, GoalCategoryPermissions, IsOwnerOrReadOnly, GoalPermissions
from to_do_list.goals.serializers import GoalCategoryCreateSerializer, GoalCategorySerializer, GoalCreateSerializer, \
    GoalSerializer, GoalCommentSerializer, GoalCommentCreateSerializer, BoardCreateSerializer, BoardListSerializer, \
    BoardSerializer
from to_do_list.goals.filters import GoalDateFilter
from django.db import transaction


class BoardCreateView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = BoardCreateSerializer

    def perform_create(self, serializer):
        """"Делаем текущего пользователя владельцем доски"""
        BoardParticipant.objects.create(user=self.request.user, board=serializer.save())


class BoardListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = BoardListSerializer
    filter_backends = [OrderingFilter]
    ordering = ['title']

    def get_queryset(self):
        return Board.objects.filter(participants__user_id=self.request.user.id, is_deleted=False)


class BoardView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = {BoardPermissions}
    serializer_class = BoardSerializer

    def get_queryset(self):
        return Board.objects.prefetch_related('participants__user').filter(is_deleted=False)

    def perform_destroy(self, instance: Board):
        with transaction.atomic():
            instance.is_deleted = True
            instance.save(update_fields=('is_deleted',))
            instance.categories.update(is_deleted=True)
            Goal.objects.filter(category__board=instance).update(
                status=Goal.Status.archived
            )
        return instance


class GoalCategoryCreateView(generics.CreateAPIView):
    permission_classes = [GoalCategoryPermissions]
    serializer_class = GoalCategoryCreateSerializer


class GoalCategoryListView(generics.ListAPIView):
    permission_classes = [GoalCategoryPermissions]
    serializer_class = GoalCategorySerializer
    filter_backends = [OrderingFilter, SearchFilter]
    ordering_fields = ['title', 'created']
    ordering = ['title']
    search_fields = ['title']

    def get_queryset(self):
        return GoalCategory.objects.select_related('user').filter(
            user=self.request.user, is_deleted=False
        )


class GoalCategoryView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [GoalCategoryPermissions]
    serializer_class = GoalCategorySerializer

    def get_queryset(self):
        return GoalCategory.objects.select_related('user').filter(
            user=self.request.user, is_deleted=False
        )

    def perform_destroy(self, instance: GoalCategory) -> None:
        with transaction.atomic():
            instance.is_deleted = True
            instance.save(update_fields=('is_deleted',))
            instance.goals.update(status=Goal.Status.archived)


class GoalCreateView(generics.CreateAPIView):
    permission_classes = [GoalPermissions]
    serializer_class = GoalCreateSerializer


class GoalListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GoalSerializer

    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_class = GoalDateFilter
    ordering_fields = ['title', 'description']
    ordering = ['title']
    search_fields = ['title', 'description']

    def get_queryset(self):
        return Goal.objects.select_related('user').filter(
            user=self.request.user, category__is_deleted=False
        ).exclude(status=Goal.Status.archived)


class GoalView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [GoalPermissions]
    serializer_class = GoalSerializer

    def get_queryset(self):
        return Goal.objects.select_related('user').filter(
            user=self.request.user, category__is_deleted=False
        ).exclude(status=Goal.Status.archived)

    def perform_destroy(self, instance: Goal):
        instance.status = Goal.Status.archived
        instance.save(update_fields=('status',))


class GoalCommentCreateView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GoalCommentCreateSerializer


class GoalCommentListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GoalCommentSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    ordering_fields = ['goal']
    ordering = ['-created']

    def get_queryset(self):
        return GoalComment.objects.select_related('user').filter(user_id=self.request.user.id)


class GoalCommentView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = GoalCommentSerializer

    def get_queryset(self):
        return GoalComment.objects.filter(user_id=self.request.user.id)
