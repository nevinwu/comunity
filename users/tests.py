from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Profile
from .forms import UserCreationForm

# Pruebas para la app de users

# Pruebas para modelos: comprueba que los perfiles de usuario se crean y manejan correctamente
class ProfileModelTest(TestCase):
    def test_profile_creation(self):
        user = User.objects.create_user(username = 'testuser', password = '12345')
        profile = Profile.objects.get(user = user)
        self.assertIsNotNone(profile) # comprueba que el perfil se crea

    def test_profile_association(self):
        user = User.objects.create_user(username = 'anotheruser', password = '12345')
        profile_exists = Profile.objects.filter(user = user).exists()
        self.assertTrue(profile_exists) # confirma que el perfil está asociado

# Pruebas para formularios: comprueba validación y manejo correo de los datos de entrada esperados
class UserCreationFormTest(TestCase):
    def test_user_creation_form_valid_data(self):
        form = UserCreationForm(data = {
            'username': 'newuser',
            'password1': 'complexpassword123',
            'password2': 'complexpassword123'
        })
        self.assertTrue(form.is_valid())

    def test_user_creation_form_invalid_data(self):
        form = UserCreationForm(data = {
            'username': 'newuser',
            'password1': 'complexpassword123',
            'password2': 'differentpassword' # passwords no coinciden
        })
        self.assertFalse(form.is_valid())

    def test_user_creation_form_empty_data(self):
        form = UserCreationForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors) # verifica que se indica el campo faltante

    def test_user_creation_form_password_mismatch(self):
        form = UserCreationForm(data={
        'username': 'newuser',
        'password1': 'complexpassword123',
        'password2': 'differentpassword'
    })
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors) # asegura que el error está en password2

# Prueba para las vistas: testea las vistas como registro, inicio de sesión y actualización de perfil
class UserViewsTest(TestCase):
    def test_register_view(self):
        url = reverse('users:register')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_login_view(self):
        url = reverse('users:login')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_profile_view_requires_login(self):
        url = reverse('users:profile')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302) # redirección al login

# Pruebas de autenticación y permisos: verifica que solo los usuarios autenticados puedan acceder a sus perfiles o editar información
class AuthenticationTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username = 'testuser', password = '12345')

    def test_login(self):
        login = self.client.login(username = 'testuser', password = '12345')
        self.assertTrue(login)

    def test_logout(self):
        self.client.login(username='testuser', password = '12345')
        response = self.client.post(reverse('users:logout'), follow = True) # sigue la redirección
        self.assertEqual(response.status_code, 200) # comprobación del destino redirigido final

    def test_profile_view_authenticated(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('users:profile'))
        self.assertEqual(response.status_code, 200) # código correcto para usuarios autenticados


