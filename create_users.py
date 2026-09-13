import os
import django

# Set up the Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'erp_poc_manager.settings')
django.setup()

from accounts.models import User
from django.contrib.auth.models import Group

# Mapping of role names to the dummy user data
USER_DATA = {
    'Administrator': {
        'username': 'admin_user',
        'email': 'admin@company.com',
        'is_staff': True,
        'is_superuser': True
    },
    'Project Manager': {
        'username': 'pm_user',
        'email': 'pm@company.com',
        'is_staff': False,
        'is_superuser': False
    },
    'Employee': {
        'username': 'employee_user',
        'email': 'employee@company.com',
        'is_staff': False,
        'is_superuser': False
    },
    'Finance': {
        'username': 'finance_user',
        'email': 'finance@company.com',
        'is_staff': False,
        'is_superuser': False
    },
    'Instructor': {
        'username': 'instructor_user',
        'email': 'instructor@company.com',
        'is_staff': False,
        'is_superuser': False
    },
    'Student': {
        'username': 'student_user',
        'email': 'student@company.com',
        'is_staff': False,
        'is_superuser': False
    },
}

def create_users_and_assign_roles():
    print("Starting to create users and assign roles...")
    
    for role_name, data in USER_DATA.items():
        # Get or create the group
        group, created = Group.objects.get_or_create(name=role_name)
        if created:
            print(f"Created group: '{role_name}'")
            
        # Create the user if they don't exist
        if not User.objects.filter(username=data['username']).exists():
            user = User.objects.create_user(
                username=data['username'],
                email=data['email'],
                password='password123'  # Default password for all dummy users
            )
            
            # Set staff/superuser status
            user.is_staff = data['is_staff']
            user.is_superuser = data['is_superuser']
            user.save()
            
            # Add user to the specific group
            user.groups.add(group)
            
            print(f"✅ Created user: '{data['username']}' and assigned to role: '{role_name}'")
        else:
            print(f"⚠️ User '{data['username']}' already exists.")
            
    print("\nUser creation script completed successfully!")

if __name__ == '__main__':
    create_users_and_assign_roles()
