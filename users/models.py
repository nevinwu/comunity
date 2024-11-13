from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    bio = models.TextField(blank = True, null = True)
    location = models.CharField(max_length = 100, blank = True, null = True)
    birth_date = models.DateField(blank = True, null = True)
    avatar = models.ImageField(upload_to = 'profile_pics/', blank = True, null = True) # foto de perfil
    created_at = models.DateTimeField(default = timezone.now) # usar timezone.now como valor por defecto
    updated_at = models.DateTimeField(auto_now = True) # fecha de última actualización
    posts = models.ManyToManyField('Post', related_name = 'profiles', blank = True)

    def clean(self):
        if self.birth_date and self.birth_date > timezone.now().date():
            raise ValidationError('La fecha de nacimiento no puede ser en el futuro.')

    def __str__(self):

        return f'{self.user.username} Profile'

# Funcionalidad de posts, no está terminado de implementar de momento
class Post(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add = True)

    def __str__(self):

        return f'Post by {self.user.username}'

