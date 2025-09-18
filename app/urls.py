from django.urls import path, include
from rest_framework import routers
from dynamic_rest.routers import DynamicRouter
from .views import RegisterView, CurrentUserView, UserViewSet, ProductViewSet, OrderViewSet, logout_view, login_view, OptionViewSet, CategoryViewSet, UnitViewSet

router = DynamicRouter()
router.register(r"products", ProductViewSet)
router.register(r"users", UserViewSet)
router.register(r"orders", OrderViewSet)
router.register(r"categories", CategoryViewSet)
router.register(r"units", UnitViewSet)
router.register(r"options", OptionViewSet)

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("logout/", logout_view, name="logout"),
    path("login/", login_view, name="login"),
    path("me/", CurrentUserView.as_view(), name="current_user"),
    path("", include(router.urls)),
]
