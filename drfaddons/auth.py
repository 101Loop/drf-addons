from rest_framework_jwt.authentication import BaseJSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication


class JSONWebTokenAuthenticationQS(BaseJSONWebTokenAuthentication):
    """
    This is a custom JWT Authentication class. This has inherited
    BaseJsonWebTokenAuthentication and also used some of the codes from
    traditional JSONWebTokenAuthentication class. The traditional one
    can only authenticate from Header with a specific key only.

    This model will first look into HEADER and if the key is not found
    there, it looks for key in the body.
    Key is also changeable and can be set in Django settings as
    JWT_AUTH_KEY with default value of Authorization.

    Source: Himanshu Shankar (https://github.com/iamhssingh)
    """
    from rest_framework_jwt.settings import api_settings
    from django.conf import settings

    key = getattr(settings, 'JWT_AUTH_KEY', 'Authorization')
    header_key = 'HTTP_' + key.upper()
    prefix = api_settings.JWT_AUTH_HEADER_PREFIX
    cookie = api_settings.JWT_AUTH_COOKIE

    def get_authorization(self, request):
        """
        This function extracts the authorization JWT string. It first
        looks for specified key in header and then looks
        for the same in body part.

        Parameters
        ----------
        request: HttpRequest
            This is the raw request that user has sent.

        Returns
        -------
        auth: str
            Return request's 'JWT_AUTH_KEY:' content from body or
            Header, as a bytestring.

            Hide some test client ickyness where the header can be unicode.
        """
        from django.utils.six import text_type
        from rest_framework import HTTP_HEADER_ENCODING

        auth = request.data.get(self.key, b'') or request.META.get(
            self.header_key, b'')

        if isinstance(auth, text_type):
            # Work around django test client oddness
            auth = auth.encode(HTTP_HEADER_ENCODING)
        return auth

    def get_jwt_value(self, request):
        """
        This function has been overloaded and it returns the proper JWT
        auth string.
        Parameters
        ----------
        request: HttpRequest
            This is the request that is received by DJango in the view.
        Returns
        -------
        str
            This returns the extracted JWT auth token string.

        """
        from django.utils.encoding import smart_text
        from django.utils.translation import ugettext as _
        from rest_framework import exceptions

        auth = self.get_authorization(request).split()
        auth_header_prefix = self.prefix.lower() or ''

        if not auth:
            if self.cookie:
                return request.COOKIES.get(self.cookie)
            return None

        if auth_header_prefix is None or len(auth_header_prefix) < 1:
            auth.append('')
            auth.reverse()

        if smart_text(auth[0].lower()) != auth_header_prefix:
            return None

        if len(auth) == 1:
            msg = _('Invalid Authorization header. No credentials provided.')
            raise exceptions.AuthenticationFailed(msg)

        elif len(auth) > 2:
            msg = _('Invalid Authorization header. Credentials string '
                    'should not contain spaces.')
            raise exceptions.AuthenticationFailed(msg)

        return auth[1]


class CsrfExemptSessionAuthentication(SessionAuthentication):
    """
    As the name suggests, it is used for CSRF Exemption. Alternative to
    @csrf_exempt
    Source: https://stackoverflow.com/a/30875830
    """

    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happening
