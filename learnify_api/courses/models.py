from django.db import models

class Instructor(models.Model):
    """Modelo para los instructores de los cursos"""
    nombre = models.CharField(max_length=200)
    especialidad = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    biografia = models.TextField(blank=True, null=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Instructor"
        verbose_name_plural = "Instructores"
        ordering = ['nombre']
    
    def __str__(self):
        return f"{self.nombre} - {self.especialidad}"


class Course(models.Model):
    """Modelo para los cursos online"""
    NIVEL_CHOICES = [
        ('principiante', 'Principiante'),
        ('intermedio', 'Intermedio'),
        ('avanzado', 'Avanzado'),
    ]
    
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    duracion = models.IntegerField(help_text="Duración en horas")
    nivel = models.CharField(max_length=20, choices=NIVEL_CHOICES)
    instructor = models.ForeignKey(
        Instructor, 
        on_delete=models.CASCADE, 
        related_name='cursos'
    )
    precio = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    activo = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Curso"
        verbose_name_plural = "Cursos"
        ordering = ['-fecha_creacion']
    
    def __str__(self):
        return f"{self.nombre} ({self.nivel})"