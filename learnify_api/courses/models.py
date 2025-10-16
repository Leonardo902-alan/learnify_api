from django.db import models

class Instructor(models.Model):
    """Modelo para instructores de cursos"""
    name = models.CharField(max_length=200, verbose_name="Nombre")
    email = models.EmailField(unique=True, verbose_name="Email")
    specialty = models.CharField(max_length=150, verbose_name="Especialidad")
    bio = models.TextField(blank=True, null=True, verbose_name="Biografía")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Instructor"
        verbose_name_plural = "Instructores"
        ordering = ['name']

    def __str__(self):
        return f"{self.name} - {self.specialty}"


class Course(models.Model):
    """Modelo para cursos online"""
    LEVEL_CHOICES = [
        ('beginner', 'Principiante'),
        ('intermediate', 'Intermedio'),
        ('advanced', 'Avanzado'),
    ]

    title = models.CharField(max_length=250, verbose_name="Título")
    description = models.TextField(verbose_name="Descripción")
    duration = models.IntegerField(verbose_name="Duración (horas)")
    level = models.CharField(
        max_length=20, 
        choices=LEVEL_CHOICES, 
        default='beginner',
        verbose_name="Nivel"
    )
    instructor = models.ForeignKey(
        Instructor, 
        on_delete=models.CASCADE, 
        related_name='courses',
        verbose_name="Instructor"
    )
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=0.00,
        verbose_name="Precio"
    )
    is_active = models.BooleanField(default=True, verbose_name="Activo")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Curso"
        verbose_name_plural = "Cursos"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.level}"