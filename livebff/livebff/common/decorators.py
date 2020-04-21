from functools import wraps

from django.shortcuts import redirect

def redirect_to_home_if_authenticated(view_fn):
    @wraps(view_fn)
    def wrapped(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        return view_fn(request, *args, **kwargs)
    return wrapped
