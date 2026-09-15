import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'll_project.settings')
django.setup()

from django.contrib.auth.models import User

username = 'admin'
email = 'cherepakhin.info7802@gmail.com'
password = 'SuperPass123!'

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username, email, password)
    print(f'Суперпользователь {username} создан.')
else:
    print(f'Суперпользователь {username} уже существует.')