from django.urls import path,include
from .views import Service
from rest_framework.routers import SimpleRouter

router = SimpleRouter()

router.register('service',Service,basename="service-api")

urlpatterns = [
    path('/',include(router.urls))
]
