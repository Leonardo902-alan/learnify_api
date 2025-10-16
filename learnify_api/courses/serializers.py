from rest_framework import serializers
from .models import Course, Instructor


class InstructorSerializer(serializers.ModelSerializer):
    """Serializador para Instructores"""
    total_courses = serializers.SerializerMethodField()
    
    class Meta:
        model = Instructor
        fields = [
            'id', 
            'name', 
            'email', 
            'specialty', 
            'bio', 
            'total_courses',
            'created_at', 
            'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def get_total_courses(self, obj):
        """Cuenta el total de cursos del instructor"""
        return obj.courses.count()


class CourseSerializer(serializers.ModelSerializer):
    """Serializador para Cursos con información del instructor"""
    instructor_name = serializers.CharField(source='instructor.name', read_only=True)
    instructor_specialty = serializers.CharField(source='instructor.specialty', read_only=True)
    level_display = serializers.CharField(source='get_level_display', read_only=True)
    
    class Meta:
        model = Course
        fields = [
            'id',
            'title',
            'description',
            'duration',
            'level',
            'level_display',
            'instructor',
            'instructor_name',
            'instructor_specialty',
            'price',
            'is_active',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def validate_duration(self, value):
        """Valida que la duración sea positiva"""
        if value <= 0:
            raise serializers.ValidationError("La duración debe ser mayor a 0 horas")
        return value

    def validate_price(self, value):
        """Valida que el precio no sea negativo"""
        if value < 0:
            raise serializers.ValidationError("El precio no puede ser negativo")
        return value


class InstructorDetailSerializer(InstructorSerializer):
    """Serializador detallado con lista de cursos"""
    courses = CourseSerializer(many=True, read_only=True)
    
    class Meta(InstructorSerializer.Meta):
        fields = InstructorSerializer.Meta.fields + ['courses']