from rest_framework.permissions import BasePermission, SAFE_METHODS
from ApiRequesters.Auth.AuthRequester import AuthRequester
from ApiRequesters.utils import get_token_from_request
from ApiRequesters.exceptions import BaseApiRequestError


class WriteOnlyBySuperuser(BasePermission):
    """
    Пермишн на запись данных только суперюзером
    """
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        try:
            token = get_token_from_request(request)
            r = AuthRequester()
            _, is_superuser = r.is_superuser(token)
            return is_superuser
        except BaseApiRequestError:
            return False
