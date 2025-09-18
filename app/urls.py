from django.urls import path, include
from rest_framework import routers
from dynamic_rest.routers import DynamicRouter
from .views import RegisterView, CurrentUserView, UserViewSet, ProductViewSet, OrderViewSet, logout_view, login_view

router = DynamicRouter()
router.register(r"products", ProductViewSet)
router.register(r"users", UserViewSet)
router.register(r"orders", OrderViewSet)

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("logout/", logout_view, name="logout"),
    path("login/", login_view, name="login"),
    path("me/", CurrentUserView.as_view(), name="current_user"),
    path("", include(router.urls)),
]
