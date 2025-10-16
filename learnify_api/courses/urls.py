from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CourseViewSet, InstructorViewSet

# Crear el router
router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='course')
router.register(r'instructors', InstructorViewSet, basename='instructor')

urlpatterns = [
    path('', include(router.urls)),
]