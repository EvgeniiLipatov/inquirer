from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import register_view, user_activate_view, UserChangeView, UserChangePasswordView, \
    UserDetailView, UserListView, password_reset_email_view, PasswordResetFormView

app_name = 'accounts'

urlpatterns = [

    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', register_view, name='register'),
    path('activate/<token>/', user_activate_view, name='user_activate'),
    path('profile/<pk>/', UserDetailView.as_view(), name='user_detail'),
    path('profile/<pk>/edit/', UserChangeView.as_view(), name='user_update'),
    path('profile/<pk>/change-password/', UserChangePasswordView.as_view(), name='user_change_password'),
    path('listuser/', UserListView.as_view(), name='user_list'),
    path('reset-password/', password_reset_email_view, name='password_reset_email'),
    path('reset-password/<token>/', PasswordResetFormView.as_view(), name='password_reset_form')
]