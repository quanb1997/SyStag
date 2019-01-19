from django.contrib.auth import get_user_model
import base64

User = get_user_model()

# this is a custom backend
class SystagBackend:
    
    def get_user(self, user_id):
        try:
            user = User._default_manager.get(pk=user_id)
        except User.DoesNotExist:
            return None
        return user

    def authenticate(self, request, username=None, password=None):
        # Check the username/password and return a user.
        ...
        if username is None:
            username = kwargs.get(User.USERNAME_FIELD)
        if password is None:
            password = kwargs.get(password)
        try:
            user = User._default_manager.get_by_natural_key(username)
        except User.DoesNotExist:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a nonexistent user (#20760).
            User().set_password(password)
        else:
            if user.check_password(password):
                return user
            # some of our users were created without hashing the passwords
            # so we will also try that
            elif user.password==password:
                return user