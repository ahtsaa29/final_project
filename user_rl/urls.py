from django.urls import path
from user_rl.views import HrmsUserRegistrationView, HrmsUserLoginView, HrmsUserProfileView, HrmsUserChangePasswordView, HrmsUserPasswordResetView, SendPasswordResetEmailView

urlpatterns = [
    # path('home/',start, name="Home page"),
    path('register/',HrmsUserRegistrationView.as_view(), name='register'),
    path('login/',HrmsUserLoginView.as_view(), name='login'),
    path('profile/',HrmsUserProfileView.as_view(), name='profile'),
    path('changepassword/', HrmsUserChangePasswordView.as_view(), name='changepassword'),
    path('send-reset-password-email/', SendPasswordResetEmailView.as_view(), name='send-reset-password-email'),
    path('reset-password/<uid>/<token>/', HrmsUserPasswordResetView.as_view(), name='reset-password'),
    # path('delete/<uid>/', HrmsUserDelete.as_view(), name='delete-user'),
]