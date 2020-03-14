from django.conf import settings
from ._AuthRequester import AuthRequester as __a, MockAuthRequester as __m

AuthRequester = __m if settings.DEBUG else __a
