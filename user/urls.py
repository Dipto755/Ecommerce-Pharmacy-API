from django.urls import path, include

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from . import views

urlpatterns = [
    path('user/register', views.CreateUserView.as_view(), name='register'),
    path('superuser/create-organization-internal', views.CreateOrganizationUserView.as_view(), name='create-organization-internal'),
    path('users', views.GetAllUserView.as_view(), name='all_user'),
    path('user/me', views.GetAndUpdateMeUserView.as_view(), name='me_user'),
    path('user/token', TokenObtainPairView.as_view(), name='token'),
    path('user/token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
]