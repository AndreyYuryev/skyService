from django.urls import path
from users.apps import UsersConfig
from django.contrib.auth.views import (LoginView, LogoutView,
                                       PasswordResetView, PasswordResetDoneView,
                                       PasswordResetConfirmView, PasswordResetCompleteView)
from users.views import (RegisterView, ProfileView, UserChangePasswordView,
                         UserChangePasswordDoneView, RecoveryView, VerificationView,
                         ActivatedView, ResetDoneView)

app_name = UsersConfig.name

urlpatterns = [
    path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('register/', RegisterView.as_view(), name='register'),
    path('recovery/', RecoveryView.as_view(), name='password_reset'),
    path('activate/<uidb64>/<token>', VerificationView.as_view(), name='activate'),
    path('activated/', ActivatedView.as_view(template_name='users/activated.html'), name='activated'),
    path('reset/done/', ResetDoneView.as_view(template_name='users/reset_done.html'), name='reset_done'),
    path('password_change/', UserChangePasswordView.as_view(), name='password_change'),
    path('password_change/done/', UserChangePasswordDoneView.as_view(), name='password_change_done'),

]
