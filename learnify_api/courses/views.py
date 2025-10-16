from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Course, Instructor
from .serializers import (
    CourseSerializer, 
    InstructorSerializer, 
    InstructorDetailSerializer
)


class CourseViewSet(viewsets.ModelViewSet):
    """
    ViewSet para CRUD completo de Cursos
    Incluye búsqueda por título y descripción
    """
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend, filters.OrderingFilter]
    search_fields = ['title', 'description', 'level']
    filterset_fields = ['level', 'instructor', 'is_active']
    ordering_fields = ['created_at', 'title', 'duration', 'price']
    ordering = ['-created_at']

    @action(detail=False, methods=['get'])
    def by_level(self, request):
        """Endpoint personalizado: cursos agrupados por nivel"""
        level = request.query_params.get('level', None)
        if level:
            courses = self.queryset.filter(level=level)
            serializer = self.get_serializer(courses, many=True)
            return Response({
                'level': level,
                'count': courses.count(),
                'courses': serializer.data
            })
        return Response({'error': 'Parámetro level requerido'}, status=400)

    @action(detail=False, methods=['get'])
    def active(self, request):
        """Obtiene solo cursos activos"""
        active_courses = self.queryset.filter(is_active=True)
        serializer = self.get_serializer(active_courses, many=True)
        return Response({
            'count': active_courses.count(),
            'courses': serializer.data
        })


class InstructorViewSet(viewsets.ModelViewSet):
    """
    ViewSet para CRUD completo de Instructores
    Incluye búsqueda por nombre y especialidad
    """
    queryset = Instructor.objects.all()
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'specialty', 'email']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']

    def get_serializer_class(self):
        """Usa serializador detallado para retrieve"""
        if self.action == 'retrieve':
            return InstructorDetailSerializer
        return InstructorSerializer

    @action(detail=True, methods=['get'])
    def courses(self, request, pk=None):
        """Obtiene todos los cursos de un instructor específico"""
        instructor = self.get_object()
        courses = instructor.courses.all()
        serializer = CourseSerializer(courses, many=True)
        return Response({
            'instructor': instructor.name,
            'specialty': instructor.specialty,
            'total_courses': courses.count(),
            'courses': serializer.data
        })