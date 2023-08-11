from django.urls import path
from .views import SimpleRegistrationView, LoginView, ForgotPasswordView, ChangePasswordView

urlpatterns = [
    path('signup', SimpleRegistrationView.as_view(), name='register'),
    path('login', LoginView.as_view(), name='login'),
    path('forgot-password', ForgotPasswordView.as_view(), name='forgot-password'),
    path('change-password', ChangePasswordView.as_view(), name='change-password'),

]
