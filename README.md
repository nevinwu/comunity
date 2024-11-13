# Comunity: Apoyo a Negocios y Causas Locales

Comunity es una aplicación web construida con Django, diseñada para apoyar negocios y causas locales mediante un sistema de donaciones y crowdfunding. Esta plataforma permite a los usuarios ver causas en las que pueden contribuir y a los negocios o creadores de causas gestionar sus perfiles y recibir apoyo de la comunidad.

## Características

- **Marketplace para negocios locales**: Los negocios pueden listar sus servicios y productos para que la comunidad los descubra. Esta funcionalidad aún no está implementada.
- **Plataforma de donaciones**: Los usuarios pueden donar a causas locales.
- **Sistema de perfiles**: Administración de perfiles de usuarios y negocios.
- **Pasarela de pago con Stripe (modo de prueba)**: La plataforma cuenta con una integración de prueba para procesar pagos.

## Configuración del Entorno de Desarrollo

### Prerrequisitos

- **Python 3.x**
- **Pipenv**: Para gestionar dependencias (si aún no lo tienes, instálalo con `pip install pipenv`)
- **SQLite**: La base de datos predeterminada es SQLite, que viene integrada con Django.
- **Claves de API de Stripe** (modo de prueba)

### Instalación

1. **Clonar el repositorio**:

   ```bash
   git clone <URL-del-repositorio>
   cd comunity
   ```

2. **Configurar las variables de entorno**:

   Crea un archivo `.env` en el directorio raíz y define las siguientes variables:

   ```plaintext
   SECRET_KEY=tu_clave_secreta_django
   STRIPE_TEST_PUBLIC_KEY=tu_clave_publica_stripe
   STRIPE_TEST_SECRET_KEY=tu_clave_secreta_stripe
   ```

3. **Instalar las dependencias**:

   Usa Pipenv para instalar las dependencias listadas en `Pipfile`:

   ```bash
   pipenv install
   ```

4. **Migrar la base de datos**:

   Ejecuta las migraciones para configurar la base de datos:

   ```bash
   pipenv run python manage.py migrate
   ```

5. **Crear un superusuario**:

   Crea una cuenta de superusuario para acceder al panel de administración de Django:

   ```bash
   pipenv run python manage.py createsuperuser
   ```

6. **Cargar datos de prueba (opcional)**:

   Si deseas cargar datos de prueba, puedes hacerlo utilizando fixtures o datos personalizados.

### Ejecución del Servidor de Desarrollo

Inicia el servidor de desarrollo con el siguiente comando:

```bash
pipenv run python manage.py runserver
```

Accede a la aplicación en [http://127.0.0.1:8000/](http://127.0.0.1:8000/).

## Uso

- Navega a la sección de causas para ver las iniciativas locales en las que puedes contribuir.
- Inicia sesión como superusuario para gestionar causas y perfiles de usuarios desde el panel de administración en `/admin`.

## Pruebas

Para ejecutar las pruebas del proyecto, usa:

```bash
pipenv run python manage.py test
```

## Notas de Seguridad

Este proyecto utiliza claves de prueba de Stripe y **no está configurado para producción**. En un entorno de producción, asegúrate de:

- Configurar `DEBUG=False` en el archivo `settings.py`.
- Usar una base de datos segura y una clave secreta única.

## Contribuciones

De momento no se aceptan contribuciones.

---

**Licencia**: Este proyecto está licenciado bajo los términos de la licencia MIT.

MIT License

Copyright (c) [2024] [Comunity]

Se concede permiso, de forma gratuita, a cualquier persona que obtenga una copia de este software y los archivos de documentación asociados (el "Software"), para utilizar el Software sin restricción, incluyendo sin limitación los derechos a usar, copiar, modificar, fusionar, publicar, distribuir, sublicenciar y/o vender copias del Software, y a permitir a las personas a las que se les proporcione el Software a hacer lo mismo, sujeto a las siguientes condiciones:

El aviso de copyright anterior y este aviso de permiso se incluirán en todas las copias o partes sustanciales del Software.

EL SOFTWARE SE PROPORCIONA "TAL CUAL", SIN GARANTÍA DE NINGÚN TIPO, EXPRESA O IMPLÍCITA, INCLUYENDO PERO NO LIMITADO A GARANTÍAS DE COMERCIALIZACIÓN, IDONEIDAD PARA UN PROPÓSITO PARTICULAR Y NO INFRACCIÓN. EN NINGÚN CASO LOS AUTORES O TITULARES DEL COPYRIGHT SERÁN RESPONSABLES DE NINGUNA RECLAMACIÓN, DAÑO U OTRA RESPONSABILIDAD, YA SEA EN UNA ACCIÓN CONTRACTUAL, AGRAVIO O DE OTRO TIPO, DERIVADA DE, FUERA O EN CONEXIÓN CON EL SOFTWARE O EL USO U OTRO TIPO DE ACCIONES EN EL SOFTWARE.
