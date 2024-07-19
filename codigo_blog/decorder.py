from functools import wraps
from django.shortcuts import redirect
from django.urls import reverse_lazy

def check_authorized(view_func):
    @wraps(view_func)
    def _wrapped_view(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return view_func(self, request, *args, **kwargs)
        if request.META.get('HTTP_REFERER') == None:
            return redirect(reverse_lazy("not_authorized"))
        return view_func(self, request, *args, **kwargs)
    return _wrapped_view