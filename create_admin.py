import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jewelry_shop.settings')
django.setup()

from django.contrib.auth.models import User

def create_admin():
    username = 'admin123@gmail.com'
    email = 'admin123@gmail.com'
    password = 'Admin@123'

    # Check if user already exists
    user = User.objects.filter(username=username).first()
    if not user:
        user = User.objects.create_superuser(username=username, email=email, password=password)
        print(f"Successfully created superuser: {username}")
    else:
        user.email = email
        user.set_password(password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        print(f"Successfully updated superuser credentials: {username}")

if __name__ == "__main__":
    create_admin()
