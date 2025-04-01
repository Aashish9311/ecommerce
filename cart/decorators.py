from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps

def buyer_required(view_func):
    """Decorator to check if the user is a buyer"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_buyer():
            messages.error(request, 'You do not have permission to access this page.')
            return redirect('home')
        return view_func(request, *args, **kwargs)
    return wrapper