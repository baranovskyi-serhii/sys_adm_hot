from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from .models import Customer

class CustomUserBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        User = get_user_model()

        try:
            user_model_1 = User.objects.get(username=username)
            if user_model_1.check_password(password):
                user_model_1.save()
                return user_model_1
        except User.DoesNotExist:
            pass
        try:
            user_model_2 = User.objects.get(email=username)
            if user_model_2.check_password(password):
                user_model_2.save()
                return user_model_2
        except User.DoesNotExist:
            pass


        return None

    def get_user(self, user_id):
        User = get_user_model()
    
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None