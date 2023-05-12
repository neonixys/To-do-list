from django.urls import path

from to_do_list.bot import views

urlpatterns = [
    path('verify', views.VerificationView.as_view(), name='verify-bot'),
]