from django.shortcuts import redirect
from django.urls import reverse

from django.shortcuts import redirect
from django.urls import reverse

def check_session(view_func):
    def _wrapped_view(request, *args, **kwargs):
        # Check if the user is authenticated
        if not request.user.is_authenticated:
            return redirect(reverse('login'))  # Replace 'home' with your home view name
        
        # Optionally, check for session key (not strictly necessary if user is authenticated)
        if not request.session.session_key:
            return redirect(reverse('login'))  # Redirect if session key is missing

        return view_func(request, *args, **kwargs)
    return _wrapped_view
