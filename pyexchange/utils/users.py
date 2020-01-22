from django.contrib.auth.models import User


def is_username_free(username: str) -> bool:
    if User.objects.filter(username=username).exists():
        return False
    return True


def is_email_free(email: str) -> bool:
    if User.objects.filter(email=email).exists():
        return False
    return True


def check_password(password) -> bool:
    if not isinstance(password, str) or len(password) == 0:
        return False
    return True
