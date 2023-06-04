from django.urls import path,include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import AccountViewset
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register("register",AccountViewset,basename="account-creation")

urlpatterns = [
    path('api/token/',TokenObtainPairView.as_view(),name="api-token-obtain"),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path("account/",include(router.urls),name="register")
]
