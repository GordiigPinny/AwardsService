from TestUtils.models import BaseTestCase
from Pins.models import Pin


class PinsListTestCase(BaseTestCase):
    """
    Тесты спискового представления (/api/pins/)
    """
    def setUp(self):
        super().setUp()
        self.path = self.url_prefix + 'pins/'
