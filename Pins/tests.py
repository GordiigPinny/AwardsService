from TestUtils.models import BaseTestCase
from Pins.models import Pin


class LocalBaseTestCase(BaseTestCase):
    """
    Локальный базовый класс тестов
    """
    def setUp(self):
        super().setUp()
        self.path = self.url_prefix + 'pins/'
        self.user_token, self.moder_token, self.super_token, self.wrong_token = \
            'user', 'moderator', 'superuser', 'nea'
        self.upin = Pin.objects.create(name='upin', ptype=Pin.USER_PIN, descr='Descr', price=100)
        self.ppin = Pin.objects.create(name='ppin', ptype=Pin.PLACE_PIN, descr='Descr', price=100)


class PinsListTestCase(LocalBaseTestCase):
    """
    Тесты спискового представления (/api/pins/)
    """
    def setUp(self):
        super().setUp()
        self.data_201 = {
            'name': 'Post',
            'ptype': Pin.USER_PIN,
            'price': 100,
        }
        self.data_400_1 = {
            'name': 'nea',
        }
        self.data_400_2 = {
            'name': 'nea',
            'price': 1,
            'ptype': 'ne',
        }

    def testGet200_Ok(self):
        response = self.get_response_and_check_status(url=self.path)
        self.fields_test(response, ['id', 'name', 'ptype', 'pic_id', 'price'])
        self.list_test(response, Pin)

    def testGet200_WithDeletedFlag(self):
        dpin = Pin.objects.create(name='ppin', ptype=Pin.PLACE_PIN, descr='Descr', price=100, deleted_flg=True)
        response = self.get_response_and_check_status(url=self.path + '?with_deleted=True')
        self.assertNotEqual(len(response), 0, msg='No content, but should be')

    def testGet200_OnlyUType(self):
        response = self.get_response_and_check_status(url=self.path + f'?ptype={Pin.USER_PIN}')
        not_u_type = list(filter(lambda x: x['ptype'] != Pin.USER_PIN, response))
        self.assertEqual(len(not_u_type), 0, msg='len(not_u_type) should be 0')

    def testGet200_OnlyPType(self):
        response = self.get_response_and_check_status(url=self.path + f'?ptype={Pin.PLACE_PIN}')
        not_p_type = list(filter(lambda x: x['ptype'] != Pin.PLACE_PIN, response))
        self.assertEqual(len(not_p_type), 0, msg='len(not_p_type) should be 0')

    def testPost201_Ok(self):
        self.token.set_role(self.token.ROLES.SUPERUSER)
        _ = self.post_response_and_check_status(url=self.path, data=self.data_201)

    def testPost401_403_NotAdminPosting(self):
        _ = self.post_response_and_check_status(url=self.path, data=self.data_201, expected_status_code=[401, 403])

    def testPost400_WrongJSON(self):
        self.token.set_role(self.token.ROLES.SUPERUSER)
        _ = self.post_response_and_check_status(url=self.path, data=self.data_400_1, expected_status_code=400)

    def testPost400_WrongPType(self):
        self.token.set_role(self.token.ROLES.SUPERUSER)
        _ = self.post_response_and_check_status(url=self.path, data=self.data_400_2, expected_status_code=400)


class PinDetailTestCase(LocalBaseTestCase):
    """
    Тесты детального представления пинов
    """
    def setUp(self):
        super().setUp()
        self.old_path = self.path
        self.path_404 = self.path + '1000000/'
        self.path += f'{self.ppin.id}/'
        self.data_202 = {
            'name': 'Post',
            'ptype': Pin.USER_PIN,
            'price': 100,
        }
        self.data_400 = {
            'name': 'nea',
            'price': -1,
        }

    def testGet200_Ok(self):
        response = self.get_response_and_check_status(url=self.path)
        self.fields_test(response, ['id', 'name', 'descr', 'ptype', 'price', 'created_dt', 'pic_id'])
        self.assertEqual(response['id'], self.ppin.id)

    def testGet200_Deleted(self):
        dpin = Pin.objects.create(name='ppin', ptype=Pin.PLACE_PIN, descr='Descr', price=100, deleted_flg=True)
        _ = self.get_response_and_check_status(url=self.old_path+f'{dpin.id}/?with_deleted=True')

    def testGet404_DeletedNoQueryparam(self):
        dpin = Pin.objects.create(name='ppin', ptype=Pin.PLACE_PIN, descr='Descr', price=100, deleted_flg=True)
        _ = self.get_response_and_check_status(url=self.old_path + f'{dpin.id}/', expected_status_code=404)

    def testGet404_WrongId(self):
        _ = self.get_response_and_check_status(url=self.path_404, expected_status_code=404)

    def testPatch202_Ok(self):
        self.token.set_role(self.token.ROLES.SUPERUSER)
        response = self.patch_response_and_check_status(url=self.path, data=self.data_202)
        self.assertEqual(response['id'], self.ppin.id)
        self.assertEqual(response['name'], self.data_202['name'])

    def testPatch401_403_NotAdminPatching(self):
        _ = self.patch_response_and_check_status(url=self.path, data=self.data_202, expected_status_code=[401, 403])

    def testPatch404_WrongId(self):
        self.token.set_role(self.token.ROLES.SUPERUSER)
        _ = self.patch_response_and_check_status(url=self.path_404, data=self.data_202, expected_status_code=404)

    def testPatch400_WrongJSON(self):
        self.token.set_role(self.token.ROLES.SUPERUSER)
        _ = self.patch_response_and_check_status(url=self.path, data=self.data_400, expected_status_code=400)

    def testDelete204_Ok(self):
        self.token.set_role(self.token.ROLES.SUPERUSER)
        _ = self.delete_response_and_check_status(url=self.path)

    def testDelete401_403_NotAdminDeleting(self):
        _ = self.delete_response_and_check_status(url=self.path, expected_status_code=[401, 403])

    def testDelete404_WrongId(self):
        self.token.set_role(self.token.ROLES.SUPERUSER)
        _ = self.delete_response_and_check_status(url=self.path_404, expected_status_code=404)
