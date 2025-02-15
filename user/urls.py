from django.urls import path

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from . import views

urlpatterns = [
    path('user/token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('user/token', TokenObtainPairView.as_view(), name='token'),
    path('user/register', views.CreateUserView.as_view(), name='register'),
    path('user/me', views.GetAndUpdateMeUserView.as_view(), name='me_user'),
    path('users', views.GetAllUserView.as_view(), name='all_user'),
    # path('superuser/create-organization-internal', views.CreateOrganizationUserView.as_view(), name='create-organization-internal'),
]