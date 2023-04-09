from django.urls import path

from to_do_list.goals import views

urlpatterns = [
    path("goal_category/create", views.GoalCategoryCreateView.as_view(), name="goal_category_create"),
    path("goal_category/list", views.GoalCategoryListView.as_view(), name="goal_category_list"),
    path("goal_category/<int:pk>", views.GoalCategoryView.as_view(), name="goal_category"),
]
