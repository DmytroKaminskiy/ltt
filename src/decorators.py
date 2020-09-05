from functools import wraps

from django.core.cache import cache


def lock_for_user(methods: tuple = ()):
    """
    lock view based on path, method and user id
    """

    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):

            if not methods or request.method in methods:
                key = f'view_lock_{request.path}_{request.method}_{request.user.id}'
                with cache.lock(key):
                    return view_func(request, *args, **kwargs)

            return view_func(request, *args, **kwargs)

        return _wrapped_view

    return decorator
