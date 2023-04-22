from django.urls import path

from to_do_list.goals import views

urlpatterns = [
    # Board
    path('board/create', views.BoardCreateView.as_view(), name='create-board'),
    path('board/list', views.BoardListView.as_view(), name='board-list'),
    path('board/<int:pk>', views.BoardView.as_view(), name='board'),

    # Goal Categories API
    path('goal_category/create', views.GoalCategoryCreateView.as_view(), name='goal_category_create'),
    path('goal_category/list', views.GoalCategoryListView.as_view(), name='goal_category_list'),
    path('goal_category/<int:pk>', views.GoalCategoryView.as_view(), name='goal_category'),

    # Goals API
    path('goal/create', views.GoalCreateView.as_view(), name='goal_create'),
    path('goal/list', views.GoalListView.as_view(), name='goal_list'),
    path('goal/<int:pk>', views.GoalView.as_view(), name='goal'),

    # Goal Comments API
    path('goal_comment/create', views.GoalCommentCreateView.as_view(), name='create-comment'),
    path('goal_comment/list', views.GoalCommentListView.as_view(), name='comment-list'),
    path('goal_comment/<int:pk>', views.GoalCommentView.as_view(), name='comment-details'),

]
