# from django.contrib.auth.backends import ModelBackend
# from school.models import PersonalInfo

# class EmailPhoneBackend(ModelBackend):

#     def authenticate(self, request, username=None, password=None, **kwargs):
#         try:
#             user = PersonalInfo.objects.get(email=username, phone_no=password)
#             return user
#         except PersonalInfo.DoesNotExist:
#             return None

#     def get_user(self, user_id):
#         try:
#             return PersonalInfo.objects.get(pk=user_id)
#         except PersonalInfo.DoesNotExist:
#             return None
