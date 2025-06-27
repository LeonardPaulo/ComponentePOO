# Pasos para Ejecutar el Proyecto

1. **Clona el repositorio**

   ```bash
   git clone https://github.com/LeonardPaulo/ComponentePOO
   cd ComponentePOO
   ```

2. **Crea y activa un entorno virtual**

   ```bash
   python -m venv .venv

   # En Git Bash:
   source .venv/bin/activate
   # En CMD de Windows:
   .venv\Scripts\activate
   # En PowerShell:
   .venv\Scripts\Activate.ps1
   ```

3. **Instala las dependencias de Python**

   ```bash
   pip install -r dependencias.txt
   ```

4. **Configura la base de datos PostgreSQL**
   - Crea la base de datos `medicos` y un usuario `postgres`.
   - Modifica la contraseña en `proy_clinico/settings.py` para que coincida con la de tu usuario de PostgreSQL:

     ```python
     DATABASES = {
         'default': {
             'ENGINE': 'django.db.backends.postgresql',
             'NAME': 'medicos',
             'USER': 'postgres',
             'PASSWORD': 'TU_CONTRASEÑA_AQUI',
             'HOST': 'localhost',
             'PORT': '5432',
         }
     }
     ```

5. **Inicia Tailwind CSS en modo observador**

   ```bash
   python manage.py tailwind start
   ```

6. **Aplica las migraciones**

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

7. **Crea un superusuario para acceder al admin**

   ```bash
   python manage.py createsuperuser
   # Usa un correo electrónico como usuario, ya que el login es por email
   ```

8. **Ejecuta el servidor de desarrollo**

   ```bash
   python manage.py runserver
   ```

9. **Accede a la aplicación**

- Sitio principal: [http://localhost:8000/](http://localhost:8000/)
- Admin de Django: [http://localhost:8000/admin/](http://localhost:8000/admin/)
- Login: [http://localhost:8000/security/signin/](http://localhost:8000/security/signin/)