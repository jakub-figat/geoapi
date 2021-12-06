from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

app_name = "user"

urlpatterns = [
    path("login/", TokenObtainPairView.as_view(), name="login"),
    path("token-refresh/", TokenRefreshView.as_view(), name="token-refresh"),
]
