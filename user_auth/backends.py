from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend

class EmailAuthBackend(BaseBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            print(f"Trying to authenticate email: {email}")  # Debug
            user = UserModel.objects.get(email=email)
            print(f"User found: {user}")  # Debug
            if user.check_password(password):
                print("Password matches")  # Debug
                # Ensure the user is active
                if user.is_active:
                    return user
                else:
                    print("User is not active")  # Debug
            else:
                print("Password does not match")  # Debug
        except UserModel.DoesNotExist:
            print("User not found")  # Debug
        return None

    def get_user(self, user_id):
        UserModel = get_user_model()
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None