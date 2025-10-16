from rest_framework import serializers
from .models import Course, Instructor


class InstructorSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Instructor"""
    total_cursos = serializers.SerializerMethodField()
    
    class Meta:
        model = Instructor
        fields = ['id', 'nombre', 'especialidad', 'email', 'biografia', 
                  'fecha_registro', 'total_cursos']
        read_only_fields = ['fecha_registro']
    
    def get_total_cursos(self, obj):
        """Retorna el número total de cursos del instructor"""
        return obj.cursos.count()


class CourseListSerializer(serializers.ModelSerializer):
    """Serializer para listar cursos (vista simplificada)"""
    instructor_nombre = serializers.CharField(source='instructor.nombre', read_only=True)
    instructor_especialidad = serializers.CharField(source='instructor.especialidad', read_only=True)
    
    class Meta:
        model = Course
        fields = ['id', 'nombre', 'duracion', 'nivel', 'precio', 
                  'instructor', 'instructor_nombre', 'instructor_especialidad', 
                  'activo', 'fecha_creacion']


class CourseDetailSerializer(serializers.ModelSerializer):
    """Serializer para detalle completo de cursos"""
    instructor_info = InstructorSerializer(source='instructor', read_only=True)
    instructor = serializers.PrimaryKeyRelatedField(
        queryset=Instructor.objects.all(),
        write_only=True
    )
    
    class Meta:
        model = Course
        fields = ['id', 'nombre', 'descripcion', 'duracion', 'nivel', 
                  'instructor', 'instructor_info', 'precio', 
                  'fecha_creacion', 'fecha_actualizacion', 'activo']
        read_only_fields = ['fecha_creacion', 'fecha_actualizacion']
    
    def validate_duracion(self, value):
        """Valida que la duración sea positiva"""
        if value <= 0:
            raise serializers.ValidationError("La duración debe ser mayor a 0 horas")
        return value
    
    def validate_precio(self, value):
        """Valida que el precio sea positivo"""
        if value < 0:
            raise serializers.ValidationError("El precio no puede ser negativo")
        return value