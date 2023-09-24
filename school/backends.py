from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from .models import PersonalInfo

class EmailPhoneAuthenticationBackend(ModelBackend):

    def authenticate(self, request, username=None, password=None, **kwargs):
        User = get_user_model()

        # Check if email and phone_no match in PersonalInfo model
        try:
            personal_info = PersonalInfo.objects.get(email=username, phone_no=password)
            return personal_info.user
        except PersonalInfo.DoesNotExist:
            pass

        return None

    def get_user(self, user_id):
        User = get_user_model()
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
