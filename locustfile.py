from locust import HttpUser, task, between
from bs4 import BeautifulSoup

class CommunityUser(HttpUser):
    wait_time = between(1, 3) # tiempo de espera entre tareas (1-3 segundos)

    def on_start(self):
        # Primero, obtenemos el CSRF token desde la página de login
        response = self.client.get("/users/login/")
        soup = BeautifulSoup(response.text, "html.parser")
        csrf_token = soup.find("input", {"name": "csrfmiddlewaretoken"})["value"]

        # Enviar login con el CSRF token
        login_data = {
            "username": "user_test",
            "password": "contraseña1234",
            "csrfmiddlewaretoken": csrf_token
        }

        response = self.client.post("/users/login/", login_data)

        # Verificar que el login haya sido exitoso
        if response.status_code == 200:
            print("Login exitoso!")
        else:
            print(f"Error al iniciar sesión: {response.status_code}")
            return # detener si el login falla

    # Vista para listar todas las causas
    @task
    def view_causa_list(self):
        self.client.get("/donations/") # página de lista de causas

    # Vista para crear una nueva causa
    @task
    def create_causa(self):
        # Obtener el CSRF token desde la página de crear causa
        response = self.client.get("/donations/causa/nueva/")
        soup = BeautifulSoup(response.text, "html.parser")
        csrf_token = soup.find("input", {"name": "csrfmiddlewaretoken"})["value"]

        # Enviar la solicitud POST para crear la causa con el token CSRF
        data = {
            'titulo': 'Causa de Prueba',
            'descripcion': 'Descripción de causa de prueba',
            'meta_recaudacion': 1000,
            'fecha_fin': '2025-12-31',
            'csrfmiddlewaretoken': csrf_token
        }
        response = self.client.post("/donations/causa/nueva/", data)

        if response.status_code == 200:
            print("Causa creada con éxito!")
        else:
            print(f"Error al crear causa: {response.status_code}")

    # Vista para realizar una donación
    @task
    def donate(self):
        causa_id = 24 # suponiendo que la causa con ID 24 existe
        # Obtener el CSRF token desde la página de donar
        response = self.client.get(f"/donations/donar/{causa_id}/")
        soup = BeautifulSoup(response.text, "html.parser")
        csrf_token = soup.find("input", {"name": "csrfmiddlewaretoken"})["value"]

        # Enviar la donación con el token CSRF
        data = {'cantidad': 50, 'csrfmiddlewaretoken': csrf_token} # donación de 50€
        response = self.client.post(f"/donations/donar/{causa_id}/", data)

        if response.status_code == 200:
            print("Donación realizada con éxito!")
        else:
            print(f"Error al realizar donación: {response.status_code}")

    # Vista de éxito de la donación
    @task
    def donacion_exitoso(self):
        donacion_id = 51 # suponiendo que la donación con ID 51 existe
        self.client.get(f"/donations/donacion_exitoso/{donacion_id}/") # página de donación exitosa

    # Vista para registrarse
    @task
    def register(self):
        # Obtener el CSRF token desde la página de registro
        response = self.client.get("/users/register/")
        soup = BeautifulSoup(response.text, "html.parser")
        csrf_token = soup.find("input", {"name": "csrfmiddlewaretoken"})["value"]

        # Enviar la solicitud POST para registrarse con el token CSRF
        data = {
            'username': 'other_user_test',
            'password1': 'password123',
            'password2': 'password123',
            'email': 'other_user_test@email.com',
            'csrfmiddlewaretoken': csrf_token
        }
        response = self.client.post("/users/register/", data)

        if response.status_code == 200:
            print("Usuario registrado con éxito!")
        else:
            print(f"Error al registrar usuario: {response.status_code}")

    # Vista de perfil de usuario
    @task
    def view_profile(self):
        self.client.get("/users/profile/") # página de perfil del usuario

    # Vista de actualización del perfil
    @task
    def update_profile(self):
        # Obtener el CSRF token desde la página de actualización de perfil
        response = self.client.get("/users/profile/update/")
        soup = BeautifulSoup(response.text, "html.parser")
        csrf_token = soup.find("input", {"name": "csrfmiddlewaretoken"})["value"]

        # Enviar la solicitud POST para actualizar el perfil con el token CSRF
        data = {
            'bio': 'Actualización de la biografía',
            'location': 'Valencia',
            'birth_date': '1990-01-01',
            'csrfmiddlewaretoken': csrf_token
        }
        response = self.client.post("/users/profile/update/", data)

        if response.status_code == 200:
            print("Perfil actualizado con éxito!")
        else:
            print(f"Error al actualizar perfil: {response.status_code}")
