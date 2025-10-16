from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Course, Instructor
from .serializers import (
    CourseListSerializer, 
    CourseDetailSerializer, 
    InstructorSerializer
)


class CourseViewSet(viewsets.ModelViewSet):
    """
    ViewSet para CRUD completo de cursos.
    Incluye búsqueda por nombre y filtro por nivel.
    """
    queryset = Course.objects.select_related('instructor').all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nombre', 'descripcion', 'nivel']
    filterset_fields = ['nivel', 'instructor', 'activo']
    ordering_fields = ['nombre', 'duracion', 'precio', 'fecha_creacion']
    ordering = ['-fecha_creacion']
    
    def get_serializer_class(self):
        """Retorna el serializer apropiado según la acción"""
        if self.action == 'list':
            return CourseListSerializer
        return CourseDetailSerializer
    
    def create(self, request, *args, **kwargs):
        """Sobrescribe el método create para personalizar la respuesta"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({
            'message': 'Curso creado exitosamente',
            'data': serializer.data
        }, status=status.HTTP_201_CREATED, headers=headers)
    
    def update(self, request, *args, **kwargs):
        """Sobrescribe el método update para personalizar la respuesta"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({
            'message': 'Curso actualizado exitosamente',
            'data': serializer.data
        })
    
    def destroy(self, request, *args, **kwargs):
        """Sobrescribe el método destroy para personalizar la respuesta"""
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({
            'message': 'Curso eliminado exitosamente'
        }, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'])
    def por_nivel(self, request):
        """Endpoint personalizado para obtener cursos agrupados por nivel"""
        niveles = {}
        for nivel_code, nivel_name in Course.NIVEL_CHOICES:
            cursos = self.queryset.filter(nivel=nivel_code, activo=True)
            niveles[nivel_name] = CourseListSerializer(cursos, many=True).data
        return Response(niveles)


class InstructorViewSet(viewsets.ModelViewSet):
    """
    ViewSet para CRUD completo de instructores.
    Incluye búsqueda por nombre y especialidad.
    """
    queryset = Instructor.objects.prefetch_related('cursos').all()
    serializer_class = InstructorSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nombre', 'especialidad']
    ordering_fields = ['nombre', 'fecha_registro']
    ordering = ['nombre']
    
    def create(self, request, *args, **kwargs):
        """Sobrescribe el método create para personalizar la respuesta"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({
            'message': 'Instructor creado exitosamente',
            'data': serializer.data
        }, status=status.HTTP_201_CREATED, headers=headers)
    
    def update(self, request, *args, **kwargs):
        """Sobrescribe el método update para personalizar la respuesta"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({
            'message': 'Instructor actualizado exitosamente',
            'data': serializer.data
        })
    
    def destroy(self, request, *args, **kwargs):
        """Sobrescribe el método destroy para personalizar la respuesta"""
        instance = self.get_object()
        cursos_count = instance.cursos.count()
        if cursos_count > 0:
            return Response({
                'error': f'No se puede eliminar el instructor porque tiene {cursos_count} curso(s) asignado(s)'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        self.perform_destroy(instance)
        return Response({
            'message': 'Instructor eliminado exitosamente'
        }, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['get'])
    def cursos(self, request, pk=None):
        """Endpoint para obtener todos los cursos de un instructor"""
        instructor = self.get_object()
        cursos = instructor.cursos.all()
        serializer = CourseListSerializer(cursos, many=True)
        return Response({
            'instructor': instructor.nombre,
            'total_cursos': cursos.count(),
            'cursos': serializer.data
        })