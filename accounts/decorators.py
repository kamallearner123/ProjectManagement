from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import user_passes_test

def in_groups(*group_names):
    """Requires user to be in at least one of the specified groups."""
    def check_user(user):
        if user.is_superuser:
            return True
        if user.groups.filter(name__in=group_names).exists():
            return True
        raise PermissionDenied("You do not have permission to view this page.")
    return user_passes_test(check_user)

def is_admin(function=None):
    return in_groups('Administrator')(function)

def is_finance(function=None):
    return in_groups('Administrator', 'Finance')(function)

def is_pm_or_admin(function=None):
    return in_groups('Administrator', 'Project Manager')(function)

def is_employee(function=None):
    return in_groups('Administrator', 'Project Manager', 'Employee')(function)

def is_lms(function=None):
    return in_groups('Administrator', 'Instructor', 'Student')(function)
