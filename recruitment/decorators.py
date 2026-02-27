from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied


def role_required(allowed_roles):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            if request.user.is_authenticated:
                if request.user.groups.filter(name__in=allowed_roles).exists():
                    return view_func(request, *args, **kwargs)
                else:
                    raise PermissionDenied
            return redirect("login")
        return wrapper
    return decorator