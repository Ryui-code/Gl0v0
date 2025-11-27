from rest_framework.authentication import BaseAuthentication
from .models import User

class CookieTokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = request.COOKIES.get('auth_token')
        if not token:
            return None

        try:
            user = User.objects.get(token=token)
        except User.DoesNotExist:
            return None
        return user, None