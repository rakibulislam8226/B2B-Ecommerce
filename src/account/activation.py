from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth import get_user_model
from django.shortcuts import render

User = get_user_model()

def activate(request, uidb64, token):
    try:
        uid = str(urlsafe_base64_decode(uidb64), 'utf-8')
        user = User.objects.get(pk=uid)
        
        if default_token_generator.check_token(user, token):
            # Activate the user account
            user.is_active = True
            user.save()
            
            # Render success page or redirect to login page
            return render(request, 'activation_success.html')
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        pass
    
    return render(request, 'activation_error.html')