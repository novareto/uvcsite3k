# PAS plugins related to secure tokens

from zope.interface import implementer
from zope.publisher.interfaces.http import IHTTPRequest
from zope.pluggableauth import interfaces


@implementer(interfaces.ICredentialsPlugin)
class TokensCredentialsPlugin(object):

    def extractCredentials(self, request):
        if not IHTTPRequest.providedBy(request):
            return None

        # this is an access token in the URL  ?access_token=...
        if not hasattr(request, 'form'):
            return None
        access_token = (request.form.get('access_token', None) or
                        request.form.get('form.field.access_token', None))
        if access_token is not None:
            return {'access_token': access_token}
        return None

    def challenge(self, request):
        return True

    def logout(self, request):
        # We might want to expire the cookie, if the token came
        # from a cookie, but it's not yet the case.
        return False
